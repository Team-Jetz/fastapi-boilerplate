from fastapi import APIRouter, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException

from sqlalchemy.orm.session import Session
from app.account.models import User
from app.authentication.oauth import get_current_user, get_token
from app.authentication.schemas import ActivateEmail, ConfirmAccountActivation, ForgotPassword, PasswordChange, PasswordReset, UserAuth
from app.authentication import views

from settings.databases import get_db
from settings.emails import send_mail
from settings.config import FRONTEND_DOMAIN


router = APIRouter(
    prefix='/auth',
    tags=['authentication']
)





@router.post('/login/')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return views.login(db, request)


@router.post('/logout/')
def logout(token: str =  Depends(get_token), db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return views.logout(db, token, current_user)


@router.post('/forgot-password/',status_code=status.HTTP_200_OK)
async def forgot_password(request: ForgotPassword = Depends(), db: Session = Depends(get_db)):
    password_reset = views.forgot_password(db, request)
    
    password_reset_link = f'{FRONTEND_DOMAIN}/forgot-password/?reset_password_token={password_reset.reset_code}'
    # Sending Password Reset Code to Email
    subject = f"PASSWORD RESET ~ {request.email}"
    recipient = [request.email]
    message = """ 
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Reset Password</title>
    </head>
    <body>
        <div style="width: 100%; font-family: monospace;">
            <h1>Hello, {0:}</h1>
            <p>
                Someone has requested a link to reset your password.  If you are the one who requested this, you can change your password through this link.
                <a href="{1:}">Reset your password here</a>
            </p>
            <p>
                If you didn't request this, you can ignore this email.
            </p>
        </div>
    </body>
    </html>
    """.format(request.email, password_reset_link)
    email_sent = await send_mail(subject, recipient, message)

    if not email_sent:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Email was not successfully sent."
        )

    return {
        "code": 200,
        "message": "An instruction to reset your password was sent to your email."
    }


@router.patch("/reset-password/")
def reset_password(request: PasswordReset = Depends(), db: Session = Depends(get_db)):
    return views.reset_password(db, request)


@router.patch('/change-password/')
def change_password(request: PasswordChange = Depends(), db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return views.change_password(db, request, current_user)


@router.post('/activate-account/')
async def activate_account(request: ActivateEmail = Depends(), db: Session = Depends(get_db)):
    account_activation = views.activate_account(db, request)

    activation_link = f'{FRONTEND_DOMAIN}/activate-account/?activation_token={account_activation.activation_code}'
    # Sending Activation Code
    subject = f"ACCOUNT ACTIVATION ~ {request.email}"
    recipient = [request.email]
    message = """ 
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Account Activation</title>
    </head>
    <body>
        <div style="width: 100%; font-family: monospace;">
            <h1>Hello, {0:}</h1>
            <p>
                Click the link in order to activate your account.
                <a href="{1:}">Activate your account here</a>
            </p>
            <p>
                If you didn't request this, you can ignore this email.
            </p>
        </div>
    </body>
    </html>
    """.format(request.email, activation_link)
    email_sent = await send_mail(subject, recipient, message)

    if not email_sent:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Email was not successfully sent."
        )
    return {
        "code": 200,
        "message": "An instruction for activating your account was sent to your email."
    }


@router.patch('/confirm-activation')
def confirm_activation(request: ConfirmAccountActivation = Depends(), db: Session = Depends(get_db)):
    return views.confirm_account_activation(db, request)