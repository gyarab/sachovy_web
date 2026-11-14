from fastapi import APIRouter
from fastapi.params import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_session, get_current_user
from backend.schemas.game import CreateGameResponseSchema
from backend.services.game import GameService

router = APIRouter(prefix="/games", tags=["Games"])

@router.get("/create", response_model=CreateGameResponseSchema)
async def create_game(session: AsyncSession = Depends(get_session), current_user = Depends(get_current_user)):
    service = GameService(session)
    pass