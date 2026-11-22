import uuid

from fastapi import APIRouter
from fastapi.params import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_session, get_current_user
from backend.schemas.game import GameResponse
from backend.services.game import GameService

router = APIRouter(prefix="/games", tags=["Games"])

@router.post("/create")
async def create_game(session: AsyncSession = Depends(get_session), current_user = Depends(get_current_user)):
    service = GameService(session)
    game = await service.create_game(current_user)
    return {"Success": True}

@router.get("/open", response_model=list[GameResponse])
async def get_open_games(session: AsyncSession = Depends(get_session)):
    service = GameService(session)
    games = await service.get_open_games()
    return games

@router.get("/{game_id}")
async def get_game(game_id: uuid.UUID, current_user = Depends(get_current_user),
                   session: AsyncSession = Depends(get_session)):
    pass

@router.post("/{game_id}/join")
async def join_game(game_id: uuid.UUID,current_user = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session)):
    pass

@router.post("/{game_id}/resign")
async def resign_game(game_id: uuid.UUID, current_user = Depends(get_current_user),
                      session: AsyncSession = Depends(get_session)):
    pass

@router.post("/{game_id}/draw_offer")
async def draw_game(game_id: uuid.UUID, current_user = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session)):
    pass

@router.post("/{game_id}/draw_accept")
async def draw_accept(game_id: uuid.UUID, current_user = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session)):
    pass

@router.post("/{game_id}/draw_decline")
async def draw_decline(game_id: uuid.UUID, current_user = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session)):
    pass

@router.delete("/{game_id}/draw_cancel")
async def draw_cancel(game_id: uuid.UUID, current_user = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session)):
    pass

@router.post("/{game_id}/move")
async def move(game_id: uuid.UUID, current_user = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session)):
    #viktor
    pass