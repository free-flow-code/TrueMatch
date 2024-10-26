import logging
from jose import jwt
from pydantic import EmailStr
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

from app.users.dao import ClientsDAO
from app.config import settings

key = settings.ENCRYPTION_KEY
cipher_suite = Fernet(key)


def get_password_hash(password: str) -> str:
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password.decode()


def get_password_from_hash(encrypted_password: str) -> str:
    decrypted_password = cipher_suite.decrypt(encrypted_password.encode())
    return decrypted_password.decode()


def verify_password(plain_password, hashed_password) -> bool:
    try:
        decrypted_password = get_password_from_hash(hashed_password)
        return plain_password == decrypted_password
    except Exception as err:
        logging.info(f"Ошибка при расшифровке пароля: {err}")
        return False


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_TOKEN_DELAY_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await ClientsDAO.find_one_or_none(email=email)

    if not user:
        return None
    if not verify_password(password, user.hash_password):
        return None
    return user
