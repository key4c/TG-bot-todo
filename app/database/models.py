from sqlalchemy import ForeignKey, String, BigInteger, select
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config import DB_URL

# Создание асинхронного движка для работы с базой данных
engine = create_async_engine(url=DB_URL, echo=True)

# Создание фабрики асинхронных сессий
async_session = async_sessionmaker(engine)


# Базовый класс для моделей
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Модель пользователя
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)

    # Связь с задачами (один пользователь может иметь много задач)
    tasks = relationship("Task", back_populates="user")


# Модель задачи
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Связь с пользователем (много задач к одному пользователю)
    user = relationship("User", back_populates="tasks")


# Асинхронная функция для создания всех таблиц
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Функция для получения задач пользователя по его Telegram ID
async def get_tasks(tg_id):
    async with async_session() as session:
        tasks = await session.scalars(
            select(Task).join(User).where(User.tg_id == tg_id)
        )
        return tasks
