import uuid
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_405_METHOD_NOT_ALLOWED

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

    async def join_game(self, game_id: uuid.UUID, player_2: uuid.UUID):
        game = await self.repo.get_game_by_id(game_id)

        if game is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Game not found")

        if game.status != "waiting":
            raise HTTPException(status_code=HTTP_405_METHOD_NOT_ALLOWED, detail="Game is already started or finished")

        if str(game.player_1_id) == player_2 or str(game.player_2_id) == player_2:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail="You're already in this game")

        await self.repo.join_game(game=game, player_2=player_2)
        await self.repo.comit()
        return game

    async def get_game_by_id(self, game_id: uuid.UUID):
        game = await self.repo.get_game_by_id(game_id)
        return game