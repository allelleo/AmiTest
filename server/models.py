from tortoise.fields import (
    DatetimeField
)
from tortoise.fields import (
    IntField, CharField, ManyToManyField, JSONField, OneToOneField
)
from tortoise.models import Model


class BaseModel(Model):
    """Абстрактный класс для моделей."""

    id = IntField(pk=True)

    class Meta:
        """Класс с метаданными полями."""

        abstract = True


class TimesBaseModel(BaseModel):
    """Абстрактный класс для моделей."""

    time_created = DatetimeField(auto_now_add=True)
    time_updated = DatetimeField(auto_now=True)

    class Meta:
        """Класс с метаданными полями."""

        abstract = True


class CheckHistory(TimesBaseModel):
    status = CharField(max_length=30)

    async def json(self):
        return {
            'id': self.id,
            'status': self.status
        }


class CheckTest(TimesBaseModel):
    history = ManyToManyField('models.CheckHistory')
    url = CharField(max_length=50)
    method = CharField(max_length=50)
    data = JSONField()
    output = JSONField()

    async def get_history(self):
        h = []
        for his in await self.history.all():
            h.append(await his.json())
        return h

    async def json(self):
        return {
            'id': self.id,
            'url': self.url,
            'method': self.method,
            'data': self.data,
            'output': self.output
        }


class ListCheck(TimesBaseModel):
    title = CharField(max_length=40)
    test = OneToOneField('models.CheckTest', null=True)
    creator = CharField(max_length=40)
    enclosure_level = IntField(default=0)

    async def json(self):
        if self.test:
            t = await (await self.test.get()).json()
        else:
            t = None
        return {
            'id': self.id,
            'title': self.title,
            'creator': self.creator,
            'test': t,
            'enclosure_level': self.enclosure_level
        }


class List(TimesBaseModel):
    title = CharField(max_length=50)
    checks = ManyToManyField('models.ListCheck')
    creator = CharField(max_length=40)

    async def json(self):
        return {
            'id': self.id,
            'title': self.title
        }

    async def get_checks(self):
        ch = []
        for c in await self.checks.all():
            ch.append(await c.json())
        return ch

    async def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'creator': self.creator,
            'checks': await self.get_checks()
        }


class BoardTag(TimesBaseModel):
    title = CharField(max_length=50)

    async def json(self):
        return {
            'id': self.id,
            'title': self.title
        }


class Board(TimesBaseModel):
    title = CharField(max_length=50)
    lists = ManyToManyField('models.List')
    creator = CharField(max_length=40)
    tags = ManyToManyField('models.BoardTag')

    async def get_tags(self):
        tags = []
        for tag in await self.tags.all():
            tags.append(await tag.json())
        return tags

    async def get_lists(self):
        lists = []
        for l in await self.lists.all():
            lists.append(await l.json())
        return lists

    async def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'tags': await self.get_tags(),
            'creator': self.creator,
            'lists': await self.get_lists(),
        }
