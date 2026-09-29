from fastapi import FastAPI
from backend.db.session import connect_db, close_db
from backend.api.routers.user import router as user_router

async def lifespan(app: FastAPI):
    await connect_db()

    yield

    await close_db()

app = FastAPI(lifespan=lifespan,
              title="Tasks Management API",
              description=
              """
some description""",
              version="1.0.0")

app.include_router(user_router)