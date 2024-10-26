import smtplib
from PIL import Image

from app.config import settings
from app.tasks.celery import celery
from app.tasks.email_templates import create_match_notification_template


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


@celery.task
def send_match_email_notification(current_client: dict, liked_client: dict):
    to_liked_client_message = create_match_notification_template(liked_client, current_client["email"])
    to_current_client_message = create_match_notification_template(current_client, liked_client["email"])

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(to_liked_client_message)
        server.send_message(to_current_client_message)
