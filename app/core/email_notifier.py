import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


class EmailNotificationManager:
    def __init__(self):
        self._smtp_user = settings.SMTP_USER
        self._sender_email = settings.NOTIFICATION_EMAIL
        self._receiver_email = settings.NOTIFICATION_EMAIL
        self._smtp = settings.SMTP_SERVER
        self._password = settings.SMTP_PASSWORD
        self._smtp_port = settings.SMTP_PORT

    def send_email(self, subject: str, body: str):
        """Send an email notification."""
        msg = MIMEMultipart()
        msg["From"] = self._sender_email
        msg["To"] = self._receiver_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(host=self._smtp, port=self._smtp_port) as server:
                server.starttls()
                server.login(user=self._smtp_user, password=self._password)
                server.send_message(msg)
            logging.info(f"✅ Email sent to {self._receiver_email} with subject: {subject}")
        except Exception as e:
            logging.error(e)