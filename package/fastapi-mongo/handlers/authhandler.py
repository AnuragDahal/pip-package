from fastapi import Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from jose import jwt
from datetime import timedelta
from utils.envutils import Environment
from handlers.exception import ErrorHandler
from utils.jwtutil import create_access_token
from handlers.userhandler import Validate

env = Environment()
SECRET_KEY = env.secret_key
ALGORITHM = env.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = env.access_token_expire_minutes
TOKEN_TYPE = env.TOKEN_TYPE
TOKEN_KEY = env.TOKEN_KEY


class AuthHandler:
    @staticmethod
    def login(request: OAuth2PasswordRequestForm = Depends()):
        user_email = Validate.verify_email(request.username)
        print(user_email)
        if user_email:
            access_token_expires = timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user_email}, expires_delta=access_token_expires)

            response = JSONResponse(
                content={"access_token": access_token,
                         "token_type": TOKEN_TYPE}
            )

            response.set_cookie(key=TOKEN_KEY, value=access_token,
                                expires=access_token_expires.total_seconds())

            return response
        return ErrorHandler.NotFound("User not found")

    @staticmethod
    def logout(res: Response):
        try:
            res.delete_cookie(TOKEN_KEY)
            return {"message": "Logged out"}
        except Exception as e:
            return ErrorHandler.NotFound(e)
