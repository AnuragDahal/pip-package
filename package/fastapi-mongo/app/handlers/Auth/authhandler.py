from fastapi import Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from jose import jwt
from datetime import timedelta, datetime, timezone
from ...utils.envutils import Environment
from ..exception import ErrorHandler
from ...utils.jwtutil import create_access_token
from ...utils.passhashutils import Encrypt
from .emailHandler import EmailHandler
from ...core.database import otp_collection, user_collection
from ...core.database import user_collection

env = Environment()
SECRET_KEY = env.SECRET_KEY
ALGORITHM = env.ALGORITHM
ACCESS_TOKEN_EXPIRE_DAYS = env.ACCESS_TOKEN_EXPIRE_DAYS
TOKEN_TYPE = env.TOKEN_TYPE
TOKEN_KEY = env.TOKEN_KEY


class Validate:
    @staticmethod
    async def verify_email(email: str):
        check_email = await user_collection.find_one({"email": email})
        if check_email:
            return True
        return False


class AuthHandler:
    @staticmethod
    async def HandleUserLogin(request: OAuth2PasswordRequestForm = Depends()):
        user_email = await user_collection.find_one({"email": request.username})
        if user_email and Encrypt.verify_password(request.password, user_email["password"]):
            access_token_expires = timedelta(
                days=ACCESS_TOKEN_EXPIRE_DAYS)
            access_token = create_access_token(
                data={"sub": user_email["email"]}, expires_delta=access_token_expires)

            response = JSONResponse(
                content={"access_token": access_token,
                         "token_type": TOKEN_TYPE}
            )

            response.set_cookie(
                key=TOKEN_KEY,
                value=access_token,
                httponly=True,
                max_age=int(access_token_expires.total_seconds()),
                expires=int(access_token_expires.total_seconds()),
                samesite="None",
                secure=True,
                path="/"
            )

            return response
        return ErrorHandler.NotFound("User not found")

    @ staticmethod
    async def HandleUserLogout(res: Response):
        try:
            res.delete_cookie(key=TOKEN_KEY)
            return {"message": "Logged out successfully"}
        except Exception as e:
            return ErrorHandler.Error(str(e))

    @staticmethod
    async def HandleForgotPassword(email: str, p: str):
        if email != p:
            return ErrorHandler.Error("Email does not match")

        user = await user_collection.find_one({"email": email})
        if not user:
            return ErrorHandler.NotFound("User not found")

        isEmailVerified = user.get("isEmailVerified", False)
        if isEmailVerified is False:  # Explicitly checking for False
            return ErrorHandler.Forbidden("Email is not verified for the process")

        token = EmailHandler.generate_email_verificaton_otp()
        # Store the otp in the database with the flag for password reset
        await otp_collection.insert_one({"email": email, "otp": token, "expires_on": datetime.now(timezone.utc), "isPasswordReset": True})
        # You need to implement this function
        htmlContent = f'''<html>
    <body>
        <p>Dear User,</p>

        <p>We recently received a request for a new login or signup associated with this email address. If you initiated this request, please enter the following verification code to confirm your identity:</p>

        <p><b>Verification Code: {token}</b></p>

        <p>If you did not initiate this request, please disregard this email and no changes will be made to your account.</p>

        <p>Thank you,<br>
        The Connectify Team</p>
    </body>
    </html>'''
        sub = "Password Reset Request"
        sendEmail = EmailHandler.send_email_to(email,htmlContent, sub)
        if not sendEmail:
            return ErrorHandler.Error("Email not sent successfully")
        return {"message": "Password reset email sent successfully"}

    @staticmethod
    async def HandlePasswordReset(email: str, password: str, confirm_password: str):
        if password != confirm_password:
            return ErrorHandler.Error("Passwords do not match")
        user = await user_collection.find_one({"email": email})
        if not user:
            return ErrorHandler.NotFound("User not found")

        hashed_password = Encrypt.hash_password(password)
        await user_collection.update_one({"email": email}, {"$set": {"password": hashed_password}})
        return {"message": "Password reset successfully"}
