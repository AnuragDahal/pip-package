from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., min_length=5, max_length=100)
