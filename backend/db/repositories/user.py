from backend.db.models import User
import uuid
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

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

    async def get_user_by_id(self, user_id):
        user = await self.session.execute(select(User).where(User.id == user_id))
        return user.scalar_one_or_none()

    async def get_leaderboard(self, current_user_id: uuid.UUID):
        if isinstance(current_user_id, str):
            current_user_id = uuid.UUID(current_user_id)

        ranked_cte = (
            select(
                User.id,
                User.name,
                User.ELO,
                User.vyhry,
                User.prohry,
                func.rank().over(order_by=User.ELO.desc()).label("rank")
            )
            .cte("ranked_users")
        )

        query = (
            select(ranked_cte)
            .where(
                or_(
                    ranked_cte.c.rank <= 10,
                    ranked_cte.c.id == current_user_id
                )
            )
            .order_by(ranked_cte.c.rank.asc())
        )

        result = await self.session.execute(query)
        rows = result.mappings().all()

        top_10 = [row for row in rows if row.rank <= 10]
        current_user_stats = next((row for row in rows if row.id == current_user_id), None)

        return {
            "leaderboard": top_10,
            "current_user": current_user_stats
        }
    async def commit(self):
        await self.session.commit()
