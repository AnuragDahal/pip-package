from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, Response, Body, Query
from pydantic import EmailStr
from typing import Annotated
from ..handlers.Auth.authhandler import AuthHandler
from ..handlers.User.userhandler import UserManager
from ..models import schemas
from ..handlers.Auth.emailHandler import EmailHandler
from ..config.dependencies import get_current_user
from ..utils.authutils import get_email_from_token
from ..handlers.exception import ErrorHandler
import re

router = APIRouter(prefix='/api/v1', tags=["Auth"])

PASSWORD_REGEX = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,16}$"


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup_user(
    name: str = Body(..., description="User's name"),
    email: EmailStr = Body(..., description="User's email"),
    password: str = Body(..., description="User's password"),
):
    # Manually validate the password
    if not re.match(PASSWORD_REGEX, password):
        return ErrorHandler.Error("Password validation failed")

    request = schemas.UserDetails(name=name, email=email, password=password)
    user = await UserManager.HandleNewUserCreation(request)
    return user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: OAuth2PasswordRequestForm = Depends()):
    user_in = await AuthHandler.HandleUserLogin(request)
    return user_in


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(res: Response, depends: str = Depends(get_current_user)):
    user_out = await AuthHandler.HandleUserLogout(res)
    return user_out


@router.post("/forgot", status_code=status.HTTP_200_OK)
async def forgot_password(email: Annotated[EmailStr, Query(..., description="Email to verify")],
                          p: EmailStr = Depends(get_email_from_token),
                          depends: str = Depends(get_current_user)):

    is_verified = await AuthHandler.HandleForgotPassword(email, p)
    return is_verified


@router.post("/reset/verify", status_code=status.HTTP_200_OK)
async def verify_password_reset_token(
        token: str = Query(...),
        email: EmailStr = Depends(get_email_from_token),
        depends: str = Depends(get_current_user)):
    flag = "isPasswordReset"
    is_verified = await EmailHandler.HandleOtpVerification(email, token, flag)
    return is_verified


@router.post("/password/reset", status_code=status.HTTP_200_OK)
async def reset_password(password: str, confirm_password: str,
                         email: EmailStr = Depends(get_email_from_token),
                         depends: str = Depends(get_current_user)):

    if not re.match(PASSWORD_REGEX, password):
        return ErrorHandler.Error("Password validation failed")
    is_reset = await AuthHandler.HandlePasswordReset(email, password, confirm_password)
    return is_reset


@router.post("/verify", status_code=status.HTTP_200_OK)
async def email_verification(email: Annotated[EmailStr, Query(..., description="Email to verify")], p: EmailStr = Depends(get_email_from_token), depends: str = Depends(get_current_user)):

    flag = "isEmailVerification"
    is_verified = await EmailHandler.HandleEmailVerification(email, p, flag)
    return is_verified


@router.post("/otp", status_code=status.HTTP_200_OK)
async def otp_verification(
    otp: Annotated[str, Query(..., description="OTP to verify")],
    email: EmailStr = Depends(get_email_from_token),
    depends: str = Depends(get_current_user)
):
    flag = "isEmailVerification"
    is_verified = await EmailHandler.HandleOtpVerification(otp, email, flag)
    return is_verified
