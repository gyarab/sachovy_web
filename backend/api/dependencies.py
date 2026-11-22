"""Zavislosti pro routery."""
import uuid

from fastapi import Cookie, Depends, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.db import session as sess
from backend.db.models import User
from backend.db.storage import storage
from backend.services.game import GameService


async def get_session():
    async with sess.SessionFactory() as session:
        yield session

async def get_current_user(session_id = Cookie(None)):
    user_id = await storage.get(f"session_id:{session_id}")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user_id

async def get_user_game(
    game_id: uuid.UUID = Path(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    game = await GameService(session).get_game_by_id(game_id)

    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )

    user_uuid = uuid.UUID(str(current_user))
    if user_uuid not in (game.player_1_id, game.player_2_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a participant in this game"
        )

    return game