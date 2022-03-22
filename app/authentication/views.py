from datetime import datetime, timedelta
import uuid
from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm.session import Session
from app.account.models import ActivationToken, PasswordReset, User

from app.account.views import check_if_email_exists, find_user_by_username
from app.authentication.oauth import create_access_token

from settings.hashing import Hash


def login(db: Session, request):
    user = db.query(User).filter(User.username==request.username, User.is_active==True).first()
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


def create_password_reset(db: Session, email, code):
    password_reset = PasswordReset(
        email = email,
        reset_code = code,
        expires_in = datetime.now() + timedelta(minutes=5)
    )
    db.add(password_reset)
    db.commit()
    db.refresh(password_reset)
    return password_reset


def forgot_password(db: Session, request):
    email_exists = check_if_email_exists(db, request.email)

    if not email_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="You have entered an invalid email address."
        )

    reset_code = str(uuid.uuid1())
    return create_password_reset(db, request.email, reset_code)


def reset_password(db: Session, request):
    if request.new_password != request.confirm_new_password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Password does not match."
        )

    reset_code_qs = db.query(PasswordReset).filter(
        PasswordReset.reset_code==request.reset_code, 
    )

    reset_code = reset_code_qs.first()
    reset_code_expired = reset_code_qs.filter(
        or_(PasswordReset.is_expired==True,PasswordReset.expires_in < datetime.utcnow())
    ).first()

    if not reset_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Reset code does not exists."
        )

    if reset_code_expired:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Reset code already expired."
        )

    user = db.query(User).filter(User.email==reset_code.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with the email of {reset_code.email} doest not exists."
        )

    reset_code.is_expired = True
    user.password = Hash.bcrypt(request.new_password)
    db.commit()

    return {
        "code": 200,
        "message":"You have successfully reset your password."
    }


def change_password(db: Session, request, current_user):
    verify_password = Hash.verify(current_user.password, request.old_password)

    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="You have entered a wrong password."
        )

    if request.new_password != request.confirm_new_password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Password does not match."
        )

    current_user.password = Hash.bcrypt(request.new_password)
    db.commit()

    return {
        "code": 200,
        "message": "You have successfully changed your password."
    }


def create_activation_code(db: Session, email, code):
    activate_account = ActivationToken(
        email = email,
        activation_code = code,
        expires_in = datetime.now() + timedelta(minutes=5)
    )
    db.add(activate_account)
    db.commit()
    db.refresh(activate_account)
    return activate_account


def activate_account(db: Session, request):
    user_qs = db.query(User).filter(User.email == request.email)
    user_activated = user_qs.filter(User.is_active == True).first()

    if not user_qs.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User with this email does not exists."
        )

    if user_activated:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Your account is already activated."
        )

    activation_code = str(uuid.uuid1())
    return create_activation_code(db, request.email, activation_code)


def confirm_account_activation(db: Session, request):
    account_activation_qs = db.query(ActivationToken).filter(
        ActivationToken.activation_code == request.activation_code
    )

    account_activation = account_activation_qs.first()
    account_activation_expired = account_activation_qs.filter(
        or_(ActivationToken.is_expired==True, ActivationToken.expires_in < datetime.utcnow())
    ).first()

    if not account_activation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Activation code does not exists."
        )

    if account_activation_expired:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Activation code already expired."
        )

    user = db.query(User).filter(User.email==account_activation.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with the email of {account_activation.email} doest not exists."
        )
    account_activation.is_expired = True
    user.is_active = True
    db.commit()

    return {
        "code":200,
        "message": "You have successfully activated your account."
    }