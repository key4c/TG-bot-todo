from app.database.models import async_session
from app.database.models import User, Task
from sqlalchemy import select, update, delete, desc


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_tasks(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            tasks = await session.scalars(select(Task).where(Task.user_id == user.id))
            return tasks
        else:
            return None
