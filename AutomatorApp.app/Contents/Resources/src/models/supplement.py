from pydantic import BaseModel, Field
from typing import Literal


class Supplement(BaseModel):
    name: str = Field(..., min_length=1)
    dosage: str = Field(..., min_length=1)
    timing: str = Field(..., min_length=1)
    priority: Literal["critical", "high", "medium", "low"]
    condition: str = Field(..., min_length=1)
