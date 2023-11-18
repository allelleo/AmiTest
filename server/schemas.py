import pydantic


class CreateBoard(pydantic.BaseModel):
    title: str
    description: str
    creator: str = 'admin'
    tags: list[str]


class CreateList(pydantic.BaseModel):
    board_id: int
    title: str
    creator: str = 'admin'


class TestCreate(pydantic.BaseModel):
    url: str
    method: str
    data: dict | list | None | str | int
    output: dict | list | None | str | int


class CreateCheck(pydantic.BaseModel):
    title: str
    creator: str = 'admin'
    enclosure_level: int = 0
    test: TestCreate | None = None
