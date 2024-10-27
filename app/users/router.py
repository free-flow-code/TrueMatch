from datetime import date
from pydantic import EmailStr
from typing import Optional
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Response, UploadFile, Form, Depends, File

from app.config import settings
from app.users.schemas import SClientAuth, SClientRegistration, SClient
from app.users.dao import ClientsDAO
from app.images.router import add_avatar
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dependencies import get_current_client
from app.users.models import ClientGender
from app.tasks.tasks import send_match_email_notification
from app.exeptions import UserAlreadyExistException, IncorrectEmailOrPasswordException, \
    LikeLimitException, FiledToLikeException

router = APIRouter(
    prefix="/clients",
    tags=["Auth & Пользователи"]
)


@router.post("/create")
async def register_client(
    email: EmailStr = Form(...),
    password: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    gender: ClientGender = Form(...),
    lat: Optional[float] = Form(None),
    lon: Optional[float] = Form(None),
    avatar: UploadFile = File(...)
):
    client_data = SClientRegistration(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        lat=lat,
        lon=lon
    )

    existing_client = await ClientsDAO.find_one_or_none(email=client_data.email)
    if existing_client:
        raise UserAlreadyExistException

    hashed_password = get_password_hash(client_data.password)
    new_client_data = client_data.dict()
    new_client_data["hash_password"] = hashed_password
    new_client_data["registration_date"] = date.today()
    new_client_data.pop("password")

    if avatar:
        new_client_data["avatar"] = await add_avatar(avatar)

    await ClientsDAO.add(**new_client_data)
    return {"message": "Клиент успешно зарегистрирован"}


@router.post("/login")
async def login_client(response: Response, user_data: SClientAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("truematch_access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout_client(response: Response):
    response.delete_cookie("truematch_access_token")


@router.post("/{id}/match")
async def match_clients(liked_client_id: int, current_client=Depends(get_current_client)):
    client_daily_likes = await ClientsDAO.count_likes_today(current_client.id)
    if client_daily_likes >= settings.DAILY_LIKES_LIMIT:
        raise LikeLimitException

    try:
        await ClientsDAO.add_like(current_client.id, liked_client_id)
    except IntegrityError:
        raise FiledToLikeException

    is_mutual_like = await ClientsDAO.check_mutual_like(current_client.id, liked_client_id)

    if is_mutual_like:
        liked_client = await ClientsDAO.find_by_id(liked_client_id)
        current_client_data = SClient.from_orm(current_client)
        liked_client_data = SClient.from_orm(liked_client)

        send_match_email_notification.delay(current_client_data.dict(), liked_client_data.dict())

        return {"message": f"Взаимная симпатия с {liked_client.email}!"}
    return {"message": "Лайк успешно отправлен!"}
