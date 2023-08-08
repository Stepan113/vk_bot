from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from create_table import User
from check_user import check_user
from add_descriptions import get_description

engine = create_engine(fr'sqlite:///vk_bot.db')
session = Session(engine, expire_on_commit=True)


def add_player(name: str):
    if check_user(name):
        user = User(name=name, description=get_description(name)[0], image='Пусто)')
        session.add(user)
        session.commit()
        return True
    else:
        return False
