import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models import Game
from backend.db.repositories.game import GameRepository
from backend.schemas.game import CreateGameSchema


class GameService:
    def __init__(self, session: AsyncSession):
        self.repo = GameRepository(session)

    async def get_user_games(self, user_id: uuid.UUID):
        games = await self.repo.get_games_by_user(user_id)
        return games

    async def create_game(self, player_1: uuid.UUID):
        game = await self.repo.create_game(game=Game(player_1_id=player_1))
        await self.repo.comit()
        return game

    async def get_open_games(self):
        games = await self.repo.get_open_games()
        return games

    async def get_game_by_id(self, game_id: uuid.UUID):
        game = await self.repo.get_game_by_id(game_id)
        return game