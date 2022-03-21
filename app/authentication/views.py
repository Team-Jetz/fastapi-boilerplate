from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from app.account.views import find_user_by_username
from app.authentication.oauth import create_access_token

from settings.hashing import Hash

def login(db: Session, request):
    user = find_user_by_username(db, request.username)
    password_verified = False

    if user:
        password_verified = Hash.verify(user.password, request.password)

    if not user or not password_verified:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Invalid credentials."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Please verify your email or contact your administrator to activate your account."
        )

    access_token = create_access_token(data={'username':user.username})

    return {
        'access_token':access_token,
        'token_type':'bearer',
        'user_id': user.id,
        'username': user.username
    }
