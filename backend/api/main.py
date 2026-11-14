from fastapi import FastAPI, APIRouter
from backend.db.session import connect_db, close_db
from backend.api.routers.user import router as user_router
from backend.api.routers.game import router as game_router

# zivotni cyklus API. Pri zapnuti pripojime DB, pri vypnuti odpojime
async def lifespan(app: FastAPI):
    await connect_db()

    yield

    await close_db()
app = FastAPI(lifespan=lifespan,
              description=
              """
some description""",
              version="1.0.0")

api_router = APIRouter(prefix="/api/v1")

# pripojeni routeru
api_router.include_router(user_router)
api_router.include_router(game_router)
app.include_router(api_router)