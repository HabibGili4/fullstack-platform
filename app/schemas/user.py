from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    email: EmailStr
    age: int = Field(ge=10, le=100)
    password: str = Field(max_length=255)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name tidak boleh kosong/spasi saja")
        return v.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        return v.lower()

    @field_validator("age")
    @classmethod
    def validate_age(cls, v):
        if v < 0:
            raise ValueError("Age tidak boleh negatif")
        return v


class UserResponse(BaseModel):
    name: str
    email: str
    age: int
    role: str


class UserListResponse(BaseModel):
    users: list[UserResponse]
    user: dict


class UserUpdate(BaseModel):
    name: str = Field(min_length=3, max_length=255)
    email: EmailStr
    age: int = Field(ge=10, le=100)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name tidak boleh kosong/spasi saja")
        return v.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        return v.lower()

    @field_validator("age")
    @classmethod
    def validate_age(cls, v):
        if v < 0:
            raise ValueError("Age tidak boleh negatif")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str
