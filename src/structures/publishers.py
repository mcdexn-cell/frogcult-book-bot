from pydantic import BaseModel


class PublisherInDb(BaseModel):
    id: int
    name: str
    mapping: list[str]
