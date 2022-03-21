from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from app.account.models import User
from settings.hashing import Hash


def find_user_by_id(db: Session, id):
    user = db.query(User).filter(User.id==id).first()
    return user


def find_user_by_username(db: Session, username):
    user = db.query(User).filter(User.username==username).first()
    return user


def check_if_username_exists(db: Session, username):
    user = db.query(User).filter(User.username==username).first()

    if user:
        return True
    return False


def check_if_email_exists(db: Session, email):
    user = db.query(User).filter(User.email==email).first()

    if user:
        return True
    return False


def create_user(db: Session, request):
    user = User(
        username=request.username,
        email=request.email,
        password= Hash.bcrypt(request.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session):
    return db.query(User).all()


def generate_superuser(db: Session, request):
    user = User(
        username=request.username,
        email=request.email,
        password= Hash.bcrypt(request.password),
        is_superuser=True,
        is_active=True,
        is_admin=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user