from pydantic import BaseModel, Field
from typing import List


class Patient(BaseModel):
    name: str = Field(..., min_length=1)
    surname: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, le=150)
    conditions: List[str] = Field(default_factory=list)
