from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from create_table import User, Game

engine = create_engine(fr'sqlite:///vk_bot.db')
session = Session(engine, expire_on_commit=True)


def select_user(name: str):
    user = session.scalar(select(User).where(User.name == name))
    game = session.scalars(select(Game).where(Game.user_fk == user.id)).all()
    res = {}
    res1 = []
    for key, value in user.__dict__.items():
        res[key] = value

    for i in game:
        for key, value in i.__dict__.items():
            if key == 'link_on_game':
                res1.append(value)
            if len(res1) == 3:
                break
    first_key = next(iter(res))
    del res[first_key]
    return [res, res1]

# print(select_user('анатолий карпов'))
