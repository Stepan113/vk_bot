from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from create_table import User

engine = create_engine(fr'sqlite:///vk_bot.db')
session = Session(engine, expire_on_commit=True)


def select_all_user():
    res = session.scalars(select(User.name)).all()
    return res
