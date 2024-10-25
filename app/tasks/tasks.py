from PIL import Image

from app.tasks.celery import celery


@celery.task
def add_watermark(base_image_path: str, watermark_image_path: str):
    base_image = Image.open(base_image_path).convert("RGBA")
    watermark = Image.open(watermark_image_path).convert("RGBA")

    position = (0, 0)
    width, height = base_image.size

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)
    transparent.save(base_image_path)
