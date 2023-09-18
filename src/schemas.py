import datetime

from pydantic import BaseModel, Field, EmailStr

from src.database.models import Role


class UserModel(BaseModel):
    username: str = Field(min_length=4, max_length=12)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    id: int = 1
    username: str = 'Unknown'
    email: str = 'unknown@example.com'
    avatar: str = 'Unknown'
    roles: Role = "user"
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr


class UserInDB(UserModel):
    hashed_password: str


class ResetPassword(BaseModel):
    reset_password_token: str
    new_password: str
    confirm_password: str
