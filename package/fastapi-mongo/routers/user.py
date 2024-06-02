from fastapi import APIRouter, status, Request, Depends, Response
from handlers.userhandler import UserManager
from typing import List
from config.dependencies import verify_token
from models import schemas
router = APIRouter(tags=["user"])


@router.post("/user", status_code=status.HTTP_201_CREATED,)
async def create_user(req: schemas.User):

    user = UserManager.create(req)
    return user


@router.get("/user", response_model=List[schemas.User], status_code=status.HTTP_200_OK,)
async def read_user():

    user = UserManager.read()
    return user


@router.patch("/update/{old_email}", response_model=schemas.User, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_token)])
async def update_user(old_email: str, request: Request, new_email: schemas.UpdateUserEmail):

    update_data = await UserManager.update(old_email, request, new_email)
    return update_data


@router.delete("/delete", status_code=status.HTTP_200_OK,)
async def delete_user(request: Request, res: Response, depends=Depends(verify_token)):

    user = await UserManager.delete(request, res)
    return user
