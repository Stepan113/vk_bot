from sqlalchemy import create_engine, select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship

engine = create_engine(fr'sqlite:///vk_bot.db')

session = Session(engine, expire_on_commit=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str]
    description: Mapped[str]
    image: Mapped[str]

    game: Mapped['Game'] = relationship(back_populates='user', uselist=True)


class Game(Base):
    __tablename__ = 'games'
    link_on_game: Mapped[str] = mapped_column(primary_key=True)

    user: Mapped['User'] = relationship(back_populates="game", uselist=False)

    user_fk: Mapped[int] = mapped_column(ForeignKey('users.id'))


Base.metadata.create_all(engine)
