import enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey

from app.database import Base


class ClientGender(enum.Enum):
    male = "male"
    female = "female"


class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    rater_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    liked_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    date = Column(Date, nullable=False)

    # Связи для получения информации о лайках
    rater = relationship("Clients", backref="likes_given", foreign_keys=[rater_id])
    liked = relationship("Clients", backref="likes_received", foreign_keys=[liked_id])


class Clients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    hash_password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    gender = Column(Enum(ClientGender), nullable=False, index=True)
    registration_date = Column(Date, nullable=False, index=True)
    avatar = Column(String)

    def __str__(self):
        return f"Пользователь {self.first_name} {self.last_name}"
