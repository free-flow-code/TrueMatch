from email.message import EmailMessage
from pydantic import EmailStr

from app.config import settings


def create_match_notification_template(match_client: dict, email_to: EmailStr):
    email = EmailMessage()
    email["Subject"] = "Взаимная симпатия!"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
        <html>
        <body>
        <h3>
            <p> Вы понравились {match_client['first_name']} {match_client['last_name']}!</p>
            <p>Почта участника {match_client['email']}</p>
        </h3>
        </body>
        </html>
        """,
        subtype="html"
    )
    return email
