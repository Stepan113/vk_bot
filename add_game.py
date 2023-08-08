from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from create_table import User, Game

engine = create_engine(fr'sqlite:///vk_bot.db')
session = Session(engine, expire_on_commit=True)


def add_game(name: str, link_on_game: str):
    user_id = session.scalar(select(User).where(User.name == name)).id
    game = Game(link_on_game=link_on_game, user_fk=user_id)
    session.add(game)
    session.commit()

# add_game('анатолий карпов', 'лрлыралвоыралы')
