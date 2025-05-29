from pydantic import BaseModel
from typing import List


class TermCreateSchema(BaseModel):
    term_kind: str
    language: str
    title: str
    pre_section: None | str = None
    sections: List[str]

    class Config:
        from_attributes = True
