from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(max_length=255)
    email: EmailStr
    age: int
