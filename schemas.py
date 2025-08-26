from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# User Schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Note Schemas
class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: str
    content: str
    version: int  # Required for version checking

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    version: int
    created_at: datetime
    updated_at: datetime
    owner_id: int
    
    class Config:
        from_attributes = True


# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
