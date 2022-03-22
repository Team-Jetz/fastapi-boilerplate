import os
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig
load_dotenv()

CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS").split(" ")

FRONTEND_DOMAIN = os.environ.get('FRONTEND_DOMAIN')

DATABASE = {
    "ENGINE" : os.environ.get('DB_BACKEND',default='postgresql'),
    "NAME" : os.environ.get('DB_NAME'),
    "USER" : os.environ.get('DB_USER'),
    "PASSWORD" : os.environ.get('DB_PASSWORD'),
    "HOST" : os.environ.get('DB_HOST',default='127.0.0.1'),
    "PORT" : os.environ.get('DB_PORT',default='5432'),
}

JWT = {
    "ACCESS_TOKEN_EXPIRE_MINUTES": os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', default='60'),
    "SECRET_KEY": os.environ.get('SECRET_KEY'),
    "ALGORITHM": os.environ.get('ALGORITHM',default='HS256')
}

S3_STORAGE = {
    "REGION" : os.environ.get('AWS_REGION'),
    "BUCKET_NAME" : os.environ.get('AWS_BUCKET_NAME'),
    "HOST_NAME" : os.environ.get('AWS_HOST_NAME'),
    "ACCESS_KEY" : os.environ.get('AWS_ACCESS_KEY'),
    "SECRET_KEY": os.environ.get('AWS_SECRET_KEY'),
}

conf = ConnectionConfig(
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD'),
    MAIL_FROM = os.environ.get('MAIL_FROM'),
    MAIL_PORT = os.environ.get('MAIL_PORT', default=587),
    MAIL_SERVER = os.environ.get('MAIL_SERVER'),
    MAIL_TLS = bool(int(os.environ.get('MAIL_TLS', default="1"))),
    MAIL_SSL = bool(int(os.environ.get('MAIL_SSL', default="0"))),
    USE_CREDENTIALS = bool(int(os.environ.get('USE_CREDENTIALS', default="1"))),
    VALIDATE_CERTS = bool(int(os.environ.get('VALIDATE_CERTS', default="1")))
)