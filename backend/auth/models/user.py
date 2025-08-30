# backend/auth/models/user.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base Pydantic model for common user fields."""
    email: EmailStr = Field(..., description="The user's email address.")
    username: str = Field(..., min_length=3, max_length=50, description="The user's unique username.")
    role: str = Field("user", description="The role of the user (e.g., 'user', 'admin').")

class UserCreate(UserBase):
    """Pydantic model for creating a new user (includes plain password)."""
    password: str = Field(..., min_length=8, description="The user's password.")

class User(UserBase):
    """Pydantic model for a User, typically used for API responses (does NOT include password_hash)."""
    id: Optional[int] = Field(None, description="Unique database ID for the user.")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp of user creation (UTC).")
    last_login: Optional[datetime] = Field(None, description="Timestamp of last login (UTC).")
    is_active: bool = Field(True, description="Indicates if the user account is active.")

    class Config:
        from_attributes = True # Allows Pydantic to read data from SQLAlchemy ORM objects

class UserInDB(UserBase):
    """Pydantic model for a User as stored in the database (includes hashed password)."""
    hashed_password: str = Field(..., description="The hashed version of the user's password.")
    id: Optional[int] = Field(None, description="Unique database ID for the user.")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp of user creation (UTC).")
    last_login: Optional[datetime] = Field(None, description="Timestamp of last login (UTC).")
    is_active: bool = Field(True, description="Indicates if the user account is active.")

    class Config:
        from_attributes = True # Allows Pydantic to read data from SQLAlchemy ORM objects

class UserUpdate(BaseModel):
    """Pydantic model for updating existing user fields."""
    email: Optional[EmailStr] = Field(None, description="New email address.")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="New username.")
    password: Optional[str] = Field(None, min_length=8, description="New plain password (will be hashed).")
    role: Optional[str] = Field(None, description="New role.")
    is_active: Optional[bool] = Field(None, description="New active status.")
