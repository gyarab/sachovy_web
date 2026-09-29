from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.db.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: User):
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_user_by_email(self, email):
        user = await self.session.execute(select(User).where(User.email == email))
        return user.scalar_one_or_none()

    async def commit(self):
        await self.session.commit()