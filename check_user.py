from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from create_table import User

engine = create_engine('sqlite:///vk_bot.db')
session = Session(engine, expire_on_commit=True)


def check_user(user: str):
    res = session.scalars(select(User).where(User.name == user)).all()
    if len(res) == 0:
        return True
    return False
