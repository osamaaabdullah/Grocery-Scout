
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from backend.core.config import get_settings

settings = get_settings()


_mail_config = ConnectionConfig(
        MAIL_USERNAME = settings.smtp_username,
        MAIL_PASSWORD = settings.smtp_password,
        MAIL_FROM = settings.smtp_mail_from,
        MAIL_PORT = settings.smtp_port,
        MAIL_SERVER = settings.smtp_mail_server,
        MAIL_FROM_NAME= settings.smtp_mail_from,
        MAIL_STARTTLS = True,
        MAIL_SSL_TLS = False,
        USE_CREDENTIALS = True
    )

_mailer = FastMail(_mail_config)

async def send_verification_email(email: str, verify_link: str) -> None:
    message = MessageSchema(
        subject="Activate your Grocery Scout Account",
        recipients=[email],
        body=f"""
            <h1>Verify your Grocery Scout Account</h1>
            <p>Please click the link below to verify your account</p>
            <a href="{verify_link}">Activate Account</a>
        """,
        subtype=MessageType.html
    )
    await _mailer.send_message(message)


async def send_password_reset_email(email: str, reset_link: str) -> None:
    message = MessageSchema(
        subject="Reset your Grocery Scout Account password",
        recipients=[email],
        body=f"""
            <h1>Reset your Grocery Scout Password</h1>
            <p>Please click the link below to reset your password</p>
            <a href="{reset_link}">Reset Password</a>
        """,
        subtype=MessageType.html
    )
    await _mailer.send_message(message)

