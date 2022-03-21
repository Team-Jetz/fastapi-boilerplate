import os
from dotenv import load_dotenv
load_dotenv()

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