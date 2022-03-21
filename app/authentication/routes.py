from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException

from sqlalchemy.orm.session import Session
from app.authentication.schemas import UserLogin
from app.authentication import views

from settings.databases import get_db

router = APIRouter(
    prefix='/auth',
    tags=['authentication']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return views.login(db, request)
