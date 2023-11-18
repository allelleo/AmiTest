import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import init
from .models import Board, BoardTag, List, ListCheck, CheckTest, CheckHistory
from .schemas import CreateBoard, CreateList, CreateCheck

app = FastAPI(title='AmiTest')
init(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/boards')
async def get_boards():
    boards = []
    for board in await Board.all():
        boards.append(await board.json())
    return boards


@app.post('/boards')
async def create_board(data: CreateBoard):
    tags = []
    for tag in data.tags:
        if await BoardTag.exists(title=tag):
            tags.append(await BoardTag.get(title=tag))
        else:
            tags.append(await BoardTag.create(title=tag))

    board = Board(
        title=data.title,
        description=data.description,
        creator=data.creator
    )
    await board.save()
    for tag in tags:
        await board.tags.add(tag)
        await board.save()
    return {'board': board.title}


@app.delete('/boards')
async def delete_board(board_id: int):
    board = await Board.get(id=board_id)
    await board.delete()
    return True


@app.get('/boards/lists')
async def get_lists(board_id: int):
    board = await Board.get(id=board_id)
    lists = await board.get_lists()
    return lists


@app.post('/boards/lists')
async def create_list(data: CreateList):
    board = await Board.get(id=data.board_id)
    L = List(
        title=data.title,
        creator=data.creator
    )
    await L.save()
    await board.lists.add(L)
    await board.save()
    return True


@app.delete('/boards/lists')
async def delete_list(list_id: int):
    L = await List.get(id=list_id)
    await L.delete()
    return True


@app.get('/boards/lists/checks')
async def get_checks(list_id: int):
    L = await List.get(id=list_id)
    return await L.get_checks()


@app.post('/boards/lists/checks')
async def create_check(list_id: int, data: CreateCheck):
    L = await List.get(id=list_id)
    check = ListCheck(
        title=data.title,
        creator=data.creator
    )
    await check.save()

    if data.test:
        test = CheckTest(
            url=data.test.url,
            method=data.test.method,
            data=data.test.data,
            output=data.test.output
        )
        await test.save()
        check.test = test
        await check.save()
    await L.checks.add(check)
    await L.save()
    return True


@app.get('/boards/lists/checks/run_test')
async def run_test(test_id: int):
    test = await CheckTest.get(id=test_id)  # получаем тест
    async with httpx.AsyncClient() as client:  # создаем клиент для запроса
        if test.method.lower() == 'get':  # проверяем указаный метод и отправляем запрос
            res = await client.get(test.url)
        elif test.method.lower() == 'post':
            if test.data:
                res = await client.post(test.url, json=test.data, data=test.data)
            else:
                res = await client.post(test.url)
    if res.status_code == 200:  # проверяем успешность запроса
        hist = await CheckHistory.create(status='ok')

        await test.history.add(hist)  # добавляем в историю запусков теста результат теста
        await test.save()

        return {
            'status': 0,
            'data': res.json()
        }
    else:
        hist = await CheckHistory.create(status='no')

        await test.history.add(hist)  # добавляем в историю запусков теста результат теста
        await test.save()
        return {
            'status': 1,
            'data': res.json()
        }


@app.get('/boards/lists/checks/tests/history')
async def get_history(test_id: int):
    test = await CheckTest.get(id=test_id)
    return await test.get_history()


@app.get('/boards/lists/checks/tests')
async def get_test(test_id: int):
    test = await CheckTest.get(id=test_id)
    return await test.json()
