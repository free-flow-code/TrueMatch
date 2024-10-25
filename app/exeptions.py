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
