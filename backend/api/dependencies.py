from backend.db import session as sess

async def get_session():
    async with sess.SessionFactory() as session:
        yield session