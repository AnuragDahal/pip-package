from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional
from datetime import datetime, timezone
from enum import Enum


class Privacy(str, Enum):
    public = "public"
    private = "private"
    friends = "friends"


class UserSignUp(BaseModel):
    name: str
    email: EmailStr
    password: constr


class OauthUser(BaseModel):
    name: str
    email: EmailStr
    isEmailVerified: Optional[bool]
    isEmailVerified: Optional[bool] = False
    friends: Optional[List[str]] = []
    profile_picture: Optional[str] = []
    posts: Optional[List[str]] = []
    commented: Optional[List[str]] = []
    comments_on_posts: Optional[List[str]] = []


class Comments(BaseModel):
    post_id: str
    comment: str
    commented_by: str = None
    commented_on: datetime = datetime.now(timezone.utc)


class Post(BaseModel):
    title: str
    content: str = None
    posted_by: EmailStr = None
    posted_on: datetime = datetime.now(timezone.utc)
    images: Optional[List[str]] = []
    likes: Optional[List[str]] = []
    comments: Optional[List[str]] = []
    privacy: Privacy = Privacy.public.value


# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid ObjectId")
#         return ObjectId(v)

class PostReceive(BaseModel):
    id: str
    title: str
    content: str = None
    posted_by: EmailStr = None
    posted_on: datetime = datetime.now(timezone.utc)
    images: Optional[List[str]] = []
    likes: Optional[List[str]] = []
    comments: Optional[List[str]] = []
    privacy: Privacy = Privacy.public.value


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    images: Optional[List[str]] = []


class UserDetails(BaseModel):
    name: str
    email: EmailStr
    password: str
    isEmailVerified: Optional[bool] = False
    friends: Optional[List[str]] = []
    friend_requests: Optional[List[str]] = []
    profile_picture: Optional[str] = str()
    # posts: Optional[List[Dict[str, Any]]] = []
    posts: Optional[List[str]] = []
    commented: Optional[List[str]] = []
    comments_on_posts: Optional[List[str]] = []


class UpdateUserEmail(BaseModel):
    email: EmailStr
