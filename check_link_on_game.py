from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from create_table import Game

engine = create_engine('sqlite:///vk_bot.db')
session = Session(engine, expire_on_commit=True)


def check_link_on_games(link: str):
    res = session.scalars(select(Game).where(Game.link_on_game == link)).all()
    if len(res) == 0:
        return True
    return False

# print(check_link_on_games('glshfjsdlsf'))
