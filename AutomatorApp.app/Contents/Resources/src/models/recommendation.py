from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class Recommendation(BaseModel):
    patient_name: str
    patient_surname: str
    date: datetime
    supplements: List["SupplementRecommendation"]


class SupplementRecommendation(BaseModel):
    name: str
    dosage: str
    timing: str
    priority: str
    reason: str
