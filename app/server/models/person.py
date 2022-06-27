from typing import Optional

from pydantic import BaseModel, Field


class PersonSchema(BaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)


class UpdatePersonModel(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "Doe",
            }
        }


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
