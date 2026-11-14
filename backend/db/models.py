from datetime import datetime
from typing import Literal

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import text
import uuid

from sqlalchemy import ForeignKey

game_status = Literal["waiting", "playing", "finished", "cancelled"]
game_result = Literal[
    "draw", "white_won", "black_won"
]

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(PGUUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    ELO: Mapped[int] = mapped_column(default=1000, server_default=text("1000"), index=True)
    vyhry: Mapped[int] = mapped_column(default=0, server_default=text("0"))
    prohry: Mapped[int] = mapped_column(default=0, server_default=text("0"))
    hash_password: Mapped[str] = mapped_column(nullable=False)

class Game(Base):
    __tablename__ = "games"
    id: Mapped[uuid.UUID] = mapped_column(PGUUID, primary_key=True, default=uuid.uuid4)
    player_1: Mapped[uuid.UUID] = mapped_column(PGUUID, ForeignKey("users.id"), nullable=False)
    player_2: Mapped[uuid.UUID] = mapped_column(PGUUID, ForeignKey("users.id"), nullable=True)
    moves: Mapped[str] = mapped_column(nullable=True, default=None)
    status: Mapped[game_status] = mapped_column(nullable=False)
    result: Mapped[game_result] = mapped_column(nullable=True, default=None)
    winner: Mapped[uuid.UUID] = mapped_column(PGUUID, ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
