from fastapi import Request, Depends
from jose import jwt, JWTError
from datetime import datetime

from app.config import settings
from app.users.dao import ClientsDAO
from app.exeptions import TokenExpiredException, TokenAbsentException, \
    IncorrectTokenFormatException, UserIsNotPresentException


def get_token(request: Request):
    token = request.cookies.get("truematch_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_client(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException

    client_id: str = payload.get("sub")
    if not client_id:
        raise UserIsNotPresentException

    client = await ClientsDAO.find_by_id(int(client_id))
    if not client:
        raise UserIsNotPresentException

    return client
