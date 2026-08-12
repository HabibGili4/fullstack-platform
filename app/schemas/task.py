from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    detail: str = Field(min_length=3)
    status: str = Field(default="pending", max_length=50)


class TaskUpdate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    detail: str = Field(min_length=3)
    status: str = Field(max_length=50)


class TaskResponse(BaseModel):
    id: int
    title: str
    detail: str
    status: str
    user_id: int
