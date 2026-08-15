from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=3)
    price: float = Field(gt=0)


class ProductUpdate(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=3)
    price: float = Field(gt=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    owner_id: int

    model_config = {"from_attributes": True}
