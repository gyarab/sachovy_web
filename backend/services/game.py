from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.repositories.game import GameRepository


class GameService:
    def __init__(self, session: AsyncSession):
        self.repo = GameRepository(session)
        
    async def create_game(self):
        pass