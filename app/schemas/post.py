from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    detail: str = Field(min_length=3)
    user_id: int


class PostUpdate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    detail: str = Field(min_length=3)


class PostResponse(BaseModel):
    id: int
    title: str
    detail: str
    user_id: int
