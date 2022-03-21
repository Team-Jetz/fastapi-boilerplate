from typing import List
from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi import HTTPException, status

from sqlalchemy.orm.session import Session
from app.account.models import User

from app.account.schemas import UserBase, UserDisplay
from app.account import views

from settings.databases import get_db

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post("/generate-superuser", status_code=status.HTTP_201_CREATED, response_model=UserDisplay)
def generate_superuser(request: UserBase, db: Session  = Depends(get_db)):
    superuser_count = db.query(User).filter(User.is_superuser==True).count()

    if superuser_count > 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='A superuser already exists.')

    return views.generate_superuser(db, request)


@router.get("/", response_model=List[UserDisplay])
def get_users(db:Session = Depends(get_db)):
    return views.get_users(db)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserDisplay)
def create_users(request: UserBase, db: Session  = Depends(get_db)):
    user_exists = views.check_if_username_exists(db, request.username)
    email_exists = views.check_if_email_exists(db, request.email)

    errors = []

    if user_exists:
        errors.append(
            {
                "loc": ["body","username"],
                "msg": "Username is not available.",
                "type": "value_error"
            }
        )

    if email_exists:
        errors.append(
            {
                "loc": ["body","email"],
                "msg": "Email is not available.",
                "type": "value_error"
            }
        )

    if len(errors) > 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=errors)

    return views.create_user(db, request)


@router.get("/{id}")
def get_user(id):
    post =  id
    return post


@router.patch("/{id}/update/")
def update_user(id):
    post =  id
    return {
        "message":"Post was successfully updated."
    }


@router.delete("/{id}/delete/")
def delete_user(id):
    post =  id
    return {
        "message":"Post was successfully deleted."
    }
