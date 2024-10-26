import os
import uuid
import aiofiles
from fastapi import APIRouter, UploadFile

from app.config import settings
from app.tasks.tasks import add_watermark

router = APIRouter(
    prefix="/images",
    tags=["Загрузка изображений"]
)


@router.post("/avatar")
async def add_avatar(file: UploadFile):
    """Асинхронная функция для загрузки аватара пользователя."""
    filename = f"{uuid.uuid4()}.png"
    os.makedirs(settings.AVATARS_DIR, exist_ok=True)
    image_path = f"{settings.AVATARS_DIR}{filename}"

    async with aiofiles.open(image_path, "wb+") as file_object:
        while True:
            content = await file.read(1024)
            if not content:
                break
            await file_object.write(content)
    add_watermark.delay(image_path, settings.WATERMARK_PATH)
    return filename
