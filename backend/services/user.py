import uuid

from fastapi import HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.auth.hash import hash_password, verify_password
from backend.db.models import User
from backend.db.repositories.user import UserRepository
from backend.db.storage import storage
from backend.schemas.user import UserRegistrationSchema, UserCredsSchema


class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def user_register(self, schema: UserRegistrationSchema):
        hash_pw = hash_password(schema.password) # hashujeme heslo
        model = User(name=schema.name, email=schema.email, hash_password=hash_pw)

        email_exist = await self.repo.get_user_by_email(
            email=schema.email) # overime, ci uz uzivatel existuje

        if email_exist is not None:
            raise HTTPException(status_code=409, detail="Email already registered")

        user = await self.repo.create_user(model)

        await self.repo.commit()

        return user

    async def auth(self, schema: UserCredsSchema, session_id: str | None = Cookie(None)):
        if session_id is not None:
            await storage.delete(f"session_id:{session_id}") # vymazame session, kdyz existuje

        user = await self.repo.get_user_by_email(schema.email)

        if user is None or not verify_password(schema.password, user.hash_password):
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        session_id = str(uuid.uuid4()) # vytvarime novy session_id

        await storage.set("session_id:" + session_id, str(user.id), ex=3600) # pridavame session do schranky

        return session_id