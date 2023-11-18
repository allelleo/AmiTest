## AmiTest

![Мы](/res/1.jpg)

### Главная фича:
```python
from fastapi import FastAPI
import httpx
import CheckTest, CheckHistory # ORM базы данных
app = FastAPI()

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
```

![Мы](/res/2.jpg)


### Наш стэк:
![Python](https://img.shields.io/badge/python-3670A0?style==flat-square&logo=python&logoColor=ffdd54)
![SQLite3](https://img.shields.io/badge/-SQLite3-%232c3e50?style=flat-square&logo=Sqlite)
![FastAPI](https://img.shields.io/badge/-FastAPI-%232c3e50?style=flat-square&logo=fastapi)
![HTML5](https://img.shields.io/badge/-HTML5-%23E44D27?style=flat-square&logo=html5&logoColor=ffffff)
![CSS3](https://img.shields.io/badge/-CSS3-%231572B6?style=flat-square&logo=css3)
![JS](https://img.shields.io/badge/-JavaScript-%231572B6?style=flat-square&logo=javascript)
