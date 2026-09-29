from fastapi import APIRouter, HTTPException
from fastapi import Response
from fastapi.params import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_session
from backend.db.storage import storage
from backend.schemas.user import UserRegistrationSchema, UserResponseSchema, UserCredsSchema
from backend.services.user import UserService

router = APIRouter(prefix="/users",tags=["User"])

@router.post(
    "/registration",
    response_model=UserResponseSchema,
    summary="Registrace",
    responses={409: {"description": "Email uz existuje"}},
)
async def user_registration(
    user: UserRegistrationSchema, session: AsyncSession = Depends(get_session)
):
    service = UserService(session)
    user = await service.user_register(user)
    return user

@router.post(
    "/auth/login",
    summary="Prihlaseni",
    responses={401: {"description": "Nespravny login nebo heslo"}},
)
async def user_login(
    user: UserCredsSchema,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    service = UserService(session)
    session_id = await service.auth(user)

    response.set_cookie(
        key="session_id",
        value=session_id,
        max_age=3600,
        httponly=True,
        samesite="lax",
    )

    return {"success": True}


@router.post(
    "/auth/logout",
    summary="Odhlaseni",
    responses={401: {"description": "Uzivatel neni prihlaseny"}},
)
async def user_logout(response: Response, session_id=Cookie(None)):
    if session_id is None:
        raise HTTPException(status_code=401, detail="User not authorized")

    response.delete_cookie(key="session_id")

    await storage.delete(f"session_id:{session_id}")

    return {"success": True}