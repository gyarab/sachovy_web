from datetime import datetime
from typing import Literal, Optional
import uuid

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

game_status = Literal["waiting", "playing", "finished", "cancelled"]
game_result = Literal["draw", "white_won", "black_won"]


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

    games_as_player_1: Mapped[list["Game"]] = relationship(
        back_populates="player_1", foreign_keys="Game.player_1_id"
    )
    games_as_player_2: Mapped[list["Game"]] = relationship(
        back_populates="player_2", foreign_keys="Game.player_2_id"
    )


class Game(Base):
    __tablename__ = "games"

    id: Mapped[uuid.UUID] = mapped_column(PGUUID, primary_key=True, default=uuid.uuid4)

    player_1_id: Mapped[uuid.UUID] = mapped_column(
        "player_1", PGUUID, ForeignKey("users.id"), nullable=False, index=True
    )
    player_2_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        "player_2", PGUUID, ForeignKey("users.id"), nullable=True, index=True
    )
    winner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        "winner", PGUUID, ForeignKey("users.id"), nullable=True
    )

    moves: Mapped[Optional[str]] = mapped_column(nullable=True, default=None)
    status: Mapped[game_status] = mapped_column(nullable=False, default="waiting")
    draw_offered_player: Mapped[PGUUID | None] = mapped_column(PGUUID, default=None, nullable=True)
    result: Mapped[Optional[game_result]] = mapped_column(nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    player_1: Mapped["User"] = relationship(
        foreign_keys=[player_1_id], back_populates="games_as_player_1"
    )
    player_2: Mapped[Optional["User"]] = relationship(
        foreign_keys=[player_2_id], back_populates="games_as_player_2"
    )
    winner: Mapped[Optional["User"]] = relationship(
        foreign_keys=[winner_id]
    )

