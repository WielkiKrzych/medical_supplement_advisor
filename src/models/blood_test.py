import math

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class BloodTest(BaseModel):
    name: str = Field(..., min_length=1)
    value: float
    unit: str = Field(..., min_length=1)
    status: Literal["low", "normal", "high"] | None = None

    @field_validator("value")
    @classmethod
    def value_must_be_finite_and_non_negative(cls, v: float) -> float:
        if not math.isfinite(v):
            raise ValueError("Blood test value must be a finite number")
        if v < 0:
            raise ValueError("Blood test value cannot be negative")
        return v
