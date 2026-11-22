import uuid

from sqlalchemy import select, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.db.models import Game, User


class GameRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_game(self, game: Game):
        self.session.add(game)
        await self.session.flush()
        return game

    async def get_games_by_user(self, user_id: uuid.UUID):
        stmt = (
            select(Game)
            .options(
                joinedload(Game.player_1),
                joinedload(Game.player_2),
                joinedload(Game.winner),
            )
            .where(
                Game.status == "finished",
                or_(
                    Game.player_1_id == user_id,
                    Game.player_2_id == user_id,
                ),
            )
            .order_by(desc(Game.created_at))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_open_games(self):
        stmt = (
            select(Game)
            .options(
                joinedload(Game.player_1)
            )
            .where(Game.status == "waiting")
            .order_by(desc(Game.created_at))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def comit(self):
        await self.session.commit()