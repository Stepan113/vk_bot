from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from create_table import User, Game

engine = create_engine(fr'sqlite:///vk_bot.db')
session = Session(engine, expire_on_commit=True)


def get_all_games(name: str):
    user_id = session.scalar(select(User).where(User.name == name)).id
    games = session.scalars(select(Game).where(Game.user_fk == user_id)).all()
    res = []
    for i in games:
        for key, value in i.__dict__.items():
            if key == 'link_on_game':
                res.append(value)
    return res


# print(get_all_games('анатолий карпов'))
