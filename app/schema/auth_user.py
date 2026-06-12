from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AuthUserCreate(BaseModel):
    name: str
    email: str
    password: str


class AuthUserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class AuthUserResponse(AuthUserCreate):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_superuser: bool
    is_feeder: bool
    is_verified: bool
    role: str

    model_config = ConfigDict(from_attributes=True)

# Payload for registering a new user.
class Register(BaseModel):
    name: str
    email: str
    password: str


# Payload for logging in an existing user.
class LoginUser(BaseModel):
    email: str
    password: str

# 