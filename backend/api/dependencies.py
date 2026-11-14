"""Zavislosti pro routery."""
from fastapi import Cookie
from backend.db import session as sess
from backend.db.storage import storage


async def get_session():
    async with sess.SessionFactory() as session:
        yield session

async def get_current_user(session_id = Cookie(None)):
    user_id = await storage.get(f"session_id:{session_id}")
    return user_id