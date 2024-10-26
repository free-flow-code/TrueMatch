from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

from app.users.models import ClientGender


class FilterParams(BaseModel):
    gender: Optional[ClientGender] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    sort_by_registration_date: Optional[bool] = False


class SClientSearch(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    first_name: str
    last_name: str
    gender: ClientGender
    registration_date: date
