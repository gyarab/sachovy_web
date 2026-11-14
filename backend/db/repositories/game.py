from sqlalchemy.ext.asyncio import AsyncSession


class GameRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_game(self):
        pass

    async def comit(self):
        await self.session.commit()