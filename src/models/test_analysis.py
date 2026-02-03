from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class ReferenceRange(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None
    unit: Optional[str] = None
    description: Optional[str] = None


class Interpretation(BaseModel):
    condition: str
    causes: List[str]
    supplements: List[str]
    priority: str
    description: Optional[str] = None


class TestAnalysis(BaseModel):
    name: str
    value: float
    unit: str
    status: str
    lab_reference: Optional[ReferenceRange] = None
    optimal_range: Optional[ReferenceRange] = None
    interpretations: List[Interpretation] = []
    possible_deficiencies: List[str] = []
    recommended_supplements: List[str] = []
    priority: str = "low"
    notes: Optional[str] = None


class SupplementRecommendation(BaseModel):
    supplement_id: str
    name: str
    dosage: str
    priority: str
    reason: str
    contraindications: List[str] = []
    interactions: List[str] = []


class CurveReading(BaseModel):
    timepoint: int
    value: float
    unit: str
    status: str


class GlucoseCurveAnalysis(BaseModel):
    readings: List[CurveReading]
    fasting_status: str
    peak_time: int
    peak_value: float
    clearance_time: Optional[int] = None
    interpretations: List[str] = []
    pattern: Optional[str] = None


class InsulinCurveAnalysis(BaseModel):
    readings: List[CurveReading]
    fasting_status: str
    peak_time: int
    peak_value: float
    clearance_time: Optional[int] = None
    interpretations: List[str] = []
    pattern: Optional[str] = None


class RatioAnalysis(BaseModel):
    name: str
    value: float
    optimal_range: str
    status: str
    interpretation: str
    supplements: List[str] = []


class MorphologyInterpretation(BaseModel):
    overall_status: str
    patterns: List[str] = []
    deficiencies: List[str] = []
    recommendations: List[str] = []


class LipidInterpretation(BaseModel):
    overall_status: str
    ratios: List[RatioAnalysis] = []
    cardiovascular_risk: str
    recommendations: List[str] = []


class ThyroidInterpretation(BaseModel):
    overall_status: str
    tsh_status: str
    ft3_percentage: Optional[float] = None
    ft4_percentage: Optional[float] = None
    autoimmune_markers: List[str] = []
    recommendations: List[str] = []


class HormoneInterpretation(BaseModel):
    overall_status: str
    ratios: List[RatioAnalysis] = []
    cycle_phase: Optional[str] = None
    recommendations: List[str] = []


class GlucoseInsulinInterpretation(BaseModel):
    overall_status: str
    insulin_resistance: bool
    glucose_curve: Optional[GlucoseCurveAnalysis] = None
    insulin_curve: Optional[InsulinCurveAnalysis] = None
    homa_ir: Optional[float] = None
    hba1c_status: Optional[str] = None
    recommendations: List[str] = []


class LiverInterpretation(BaseModel):
    overall_status: str
    ast_alt_ratio: Optional[float] = None
    pattern: Optional[str] = None
    recommendations: List[str] = []


class ComprehensiveAnalysis(BaseModel):
    patient_name: str
    patient_surname: str
    test_date: Optional[str] = None

    morphology: Optional[MorphologyInterpretation] = None
    inflammatory_markers: List[TestAnalysis] = []
    minerals_vitamins: List[TestAnalysis] = []
    electrolytes: List[TestAnalysis] = []
    thyroid: Optional[ThyroidInterpretation] = None
    glucose_insulin: Optional[GlucoseInsulinInterpretation] = None
    lipids: Optional[LipidInterpretation] = None
    liver: Optional[LiverInterpretation] = None
    hormones: Optional[HormoneInterpretation] = None

    all_supplements: List[SupplementRecommendation] = []
    critical_issues: List[str] = []
    recommendations_summary: List[str] = []
