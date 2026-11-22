import uuid

from fastapi import APIRouter
from fastapi.params import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_session, get_current_user, get_user_game
from backend.db.models import Game
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

@router.get("/{game_id}", response_model=GameResponse,)
async def get_game(game_id: uuid.UUID,
                    session: AsyncSession = Depends(get_session)):
    service = GameService(session)
    game = await service.get_game_by_id(game_id)
    return game

@router.patch("/{game_id}/join")
async def join_game(game_id: uuid.UUID, current_user = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session)):
    service = GameService(session)
    await service.join_game(game_id, current_user)
    return {"Success": True}

@router.post("/{game_id}/resign")
async def resign_game(game: Game = Depends(get_user_game), current_user = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session)):
    pass

@router.patch("/{game_id}/draw_offer")
async def draw_game(game: Game = Depends(get_user_game), current_user = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session)):
    service = GameService(session)
    await service.draw_offer(game, current_user)
    return {"Success": True}

@router.post("/{game_id}/draw_accept")
async def draw_accept(game: Game = Depends(get_user_game), current_user = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session)):
    service = GameService(session)
    await service.draw_game(game, current_user)
    return {"Success": True}

@router.post("/{game_id}/draw_decline")
async def draw_decline(game: Game = Depends(get_user_game), current_user = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session)):
    service = GameService(session)
    await service.draw_decline(game, current_user)
    return {"Success": True}

@router.patch("/{game_id}/draw_cancel")
async def draw_cancel(game: Game = Depends(get_user_game), current_user = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session)):
    service = GameService(session)
    await service.draw_cancel(game, current_user)
    return {"Success": True}

@router.post("/{game_id}/move")
async def move(game: Game = Depends(get_user_game),
                    session: AsyncSession = Depends(get_session)):
    #viktor
    pass