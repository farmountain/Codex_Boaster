# backend/auth/models.py

from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    """
    Pydantic model for a User, typically used for response bodies
    or when retrieving user data.
    """
    id: str = Field(..., description="Unique identifier for the user.")
    username: str = Field(..., description="The user's unique username.")
    email: Optional[str] = Field(None, description="The user's email address.")
    role: Optional[str] = Field("user", description="The role of the user (e.g., 'user', 'admin').")
    is_active: bool = Field(True, description="Indicates if the user account is active.")

    class Config:
        # Allows ORM mode for SQLAlchemy/etc. integration (if applicable)
        from_attributes = True

class UserCreate(BaseModel):
    """
    Pydantic model for creating a new user,
    used for request bodies where password is required.
    """
    username: str = Field(..., min_length=3, max_length=50, description="The desired username for the new user.")
    password: str = Field(..., min_length=8, description="The user's password.")
    email: Optional[str] = Field(None, description="The user's email address.")
    role: Optional[str] = Field("user", description="The initial role for the new user.")

class UserInDB(User):
    """
    Pydantic model for a User stored in the database,
    including the hashed password.
    """
    hashed_password: str = Field(..., description="The hashed version of the user's password.")

