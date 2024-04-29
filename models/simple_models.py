from pydantic import BaseModel, Field
from typing import Union, Annotated


class SimpleBook(BaseModel):
    id: int
    title: str
    release_year: Annotated[Union[int, None], Field(default=1900, gt=1600, lt=2024)]
    author_id: int


class SimpleAuthor(BaseModel):
    id: int
    name: str
    birth_year: Annotated[Union[int, None], Field(default=2000, gt=1600, lt=2024)]


class SimpleAuthorPath(BaseModel):
    id: int
    name: Union[str, None] = None
    birth_year: Annotated[Union[int, None], Field(default=2000, gt=1600, lt=2024)]