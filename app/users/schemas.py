from pydantic import BaseModel, ConfigDict, EmailStr

from app.users.models import ClientGender


class SClientRegistration(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    password: str
    first_name: str
    last_name: str
    gender: ClientGender


class SClientAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    password: str


class SClient(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    first_name: str
    last_name: str
