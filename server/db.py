"""Файл с настройками для базы данных."""

from tortoise.contrib.fastapi import register_tortoise




def init(app):
    """Функция для инициализации базы данных."""
    register_tortoise(
        app,
        db_url="sqlite://database1.db",
        modules={"models": ['app.models']},
        generate_schemas=True,
        add_exception_handlers=True,
    )
