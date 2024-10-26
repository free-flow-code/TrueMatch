from datetime import date
from sqlalchemy import func, select, cast, Integer, Date

from app.dao.base import BaseDAO
from app.users.models import Clients, Likes
from app.database import async_session_maker
from app.search.schemas import FilterParams


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

    @classmethod
    async def list_clients(cls, filters: FilterParams, skip: int = 0, limit: int = 10):
        async with async_session_maker() as session:
            query = select(Clients)

            if filters.gender:
                query = query.filter(Clients.gender == filters.gender)

            if filters.first_name:
                query = query.filter(Clients.first_name.ilike(f"%{filters.first_name}%"))

            if filters.last_name:
                query = query.filter(Clients.last_name.ilike(f"%{filters.last_name}%"))

            if filters.sort_by_registration_date:
                query = query.order_by(Clients.registration_date)

            query = query.offset(skip).limit(limit)

            result = await session.execute(query)
            clients = result.scalars().all()

        return clients
