from typing import List
from fastapi_mail import FastMail, MessageSchema
from settings.config import conf

async def send_mail(subject: str, email: List, message):
    try:

        email_message = MessageSchema(
            subject = subject,
            recipients = email,
            body=message,
            subtype="html"
            )
        fm = FastMail(conf)
        await fm.send_message(email_message)

        return True
    except:
        return False