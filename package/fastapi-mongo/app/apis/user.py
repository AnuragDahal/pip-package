from fastapi import APIRouter, status,  Depends, Response, UploadFile, File, Form, Query, Path
from ..handlers.User.userhandler import UserManager
from ..handlers.User.uploadhandler import UploadManager
from typing import List
from pydantic import EmailStr
from ..config.dependencies import get_current_user
from ..models import schemas
from ..utils.authutils import get_email_from_token

router = APIRouter(prefix='/api/v1', tags=["Users"],
                   )


@router.get("/user", response_model=List[schemas.UserDetails], status_code=status.HTTP_200_OK,)
async def read_user():

    user = await UserManager.HandleReadingUserRecords()
    return user


@router.post("/profile", dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK)
async def upload_profile_pic(img: UploadFile = File(...), email: EmailStr = Depends(get_email_from_token)):

    img_upload = await UploadManager.HandleUploadProfilePic(email, img)
    return img_upload


@router.delete("/delete", dependencies=[Depends(get_current_user)], status_code=status.HTTP_200_OK,)
async def delete_user(res: Response, email: EmailStr = Depends(get_email_from_token), password: str =
                      Form(..., description="Enter the password to delete"), depends=Depends(get_current_user)):

    user = await UserManager.HandleUserDeletion(email, password, res)
    return user
