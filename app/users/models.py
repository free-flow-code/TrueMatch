import enum
from sqlalchemy import Column, Integer, String, Date, Enum

from app.database import Base


class ClientGender(enum.Enum):
    male = "male"
    female = "female"


class Clients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    hash_password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(Enum(ClientGender), nullable=False)
    registration_date = Column(Date, nullable=False)
    avatar = Column(String)

    def __str__(self):
        return f"Пользователь {self.first_name} {self.last_name}"
