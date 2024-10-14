from pydantic import BaseModel


class CreateAdv(BaseModel):
    head: str
    description: str
    owner: str


class UpdateAdv(BaseModel):
    head: str | None = None
    description: str | None = None
    owner: str | None = None
