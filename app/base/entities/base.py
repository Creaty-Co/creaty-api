from pydantic import BaseModel as PydanticModel


class BaseEntity(PydanticModel):
    class Config:
        arbitrary_types_allowed = True
