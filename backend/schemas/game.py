import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from backend.db.models import game_status, game_result

class CreateGameSchema(BaseModel):
    player_1_id: uuid.UUID

class PlayerShortInfo(BaseModel):
    id: uuid.UUID
    name: str
    ELO: int
    model_config = ConfigDict(from_attributes=True)

class GameResponse(BaseModel):
    id: uuid.UUID
    status: game_status
    result: Optional[game_result] = None
    moves: Optional[str] = None
    created_at: datetime

    player_1: PlayerShortInfo
    player_2: Optional[PlayerShortInfo] = None
    winner: Optional[PlayerShortInfo] = None

    model_config = ConfigDict(from_attributes=True)