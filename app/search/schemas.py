from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.users.models import ClientGender


class FilterParams(BaseModel):
    gender: Optional[ClientGender] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    sort_by_registration_date: Optional[bool] = False
    max_distance: Optional[float] = Field(None, description="Maximum distance in kilometers")


class SClientSearch(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    first_name: str
    last_name: str
    gender: ClientGender
    registration_date: date
