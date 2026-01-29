from pydantic import BaseModel, Field
from typing import Literal


class BloodTest(BaseModel):
    name: str = Field(..., min_length=1)
    value: float
    unit: str = Field(..., min_length=1)
    status: Literal["low", "normal", "high"] | None = None
