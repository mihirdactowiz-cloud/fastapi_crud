# schemas.py
from pydantic import BaseModel

# Create User Schema
class UserCreate(BaseModel):
    name: str
    email: str
    age: int

# Response Schema
class UserResponse(UserCreate):
    id: int
    class Config:
        from_attributes = True