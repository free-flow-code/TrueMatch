from fastapi import HTTPException, status

UserAlreadyExistException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует.",
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверная почта или пароль.",
)

AvatarDownloadException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Ошибка загрузки аватара.",
)

LikeLimitException = HTTPException(
    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    detail="Превышен дневной лимит лайков."
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истек.",
)

TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен отсутствует.",
)

IncorrectTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный формат токена.",
)

UserIsNotPresentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
)

FiledToLikeException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Не удалось поставить лайк."
)
