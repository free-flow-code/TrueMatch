import logging
from datetime import date
from pydantic import EmailStr
from fastapi import APIRouter, Response, UploadFile, Form

from app.users.schemas import SClientAuth, SClientRegistration
from app.users.dao import ClientsDAO
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.images.router import add_avatar
from app.users.models import ClientGender
from app.exeptions import UserAlreadyExistException, IncorrectEmailOrPasswordException, AvatarDownloadException

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
    avatar: UploadFile = None
):
    client_data = SClientRegistration(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        gender=gender
    )

    existing_client = await ClientsDAO.find_one_or_none(email=client_data.email)
    if existing_client:
        raise UserAlreadyExistException

    hashed_password = get_password_hash(client_data.password)
    new_client_data = client_data.dict()
    new_client_data["hash_password"] = hashed_password
    new_client_data["registration_date"] = date.today()
    new_client_data.pop("password")

    # Загружаем аватар
    try:
        avatar_filename = await add_avatar(avatar)
        new_client_data["avatar"] = avatar_filename
    except Exception as err:
        logging.info(f"{err}")
        raise AvatarDownloadException

    await ClientsDAO.add(**new_client_data)
    return {"message": "Клиент успешно зарегистрирован"}


@router.post("/login")
async def login_client(response: Response, user_data: SClientAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout_client(response: Response):
    response.delete_cookie("booking_access_token")