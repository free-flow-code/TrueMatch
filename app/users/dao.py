from datetime import date
from sqlalchemy import func, select, cast, Integer, Date

from app.dao.base import BaseDAO
from app.users.models import Clients, Likes
from app.database import async_session_maker


class ClientsDAO(BaseDAO):
    model = Clients

    @classmethod
    async def count_likes_today(cls, client_id: int):
        async with async_session_maker() as session:
            today = date.today()
            query = select(func.count(Likes.id)).filter(
                Likes.rater_id == cast(client_id, Integer),
                Likes.date == cast(today, Date)
            )
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def add_like(cls, rater_id: int, liked_id: int):
        async with async_session_maker() as session:
            new_like = Likes(rater_id=rater_id, liked_id=liked_id, date=date.today())
            session.add(new_like)
            await session.commit()

    @classmethod
    async def check_mutual_like(cls, client_id: int, liked_client_id: int):
        async with async_session_maker() as session:
            query = select(Likes).filter(
                Likes.rater_id == cast(liked_client_id, Integer),
                Likes.liked_id == cast(client_id, Integer)
            )
            result = await session.execute(query)
            return result.scalar() is not None
