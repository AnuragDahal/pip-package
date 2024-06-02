from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, Response
from handlers.authhandler import AuthHandler
router = APIRouter(tags=["auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: OAuth2PasswordRequestForm = Depends()):

    user_in = AuthHandler.login(request)
    return user_in


@router.post("/logout")
async def logout(res: Response):

    user_out = AuthHandler.logout(res)
    return user_out
