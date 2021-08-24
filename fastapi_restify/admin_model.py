from pydantic import BaseModel, Field, EmailStr


class AdminModel(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    password2: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Test User",
                "email": "me@x.com",
                "password": "me",
                "password2": "me"
            }
        }
