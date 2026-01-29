from src.models.patient import Patient
from src.models.blood_test import BloodTest
from src.models.recommendation import Recommendation, SupplementRecommendation
from src.core.analyzer import Analyzer
from src.core.rule_engine import RuleEngine
from typing import List, Dict
from datetime import datetime
from config import PRIORITY_ORDER


class RecommendationEngine:
    """Generates supplement recommendations based on blood test analysis.

    Combines blood test analysis with dosage and timing rules
    to create prioritized supplement recommendations for patients.
    """

    def __init__(
        self,
        reference_ranges: Dict,
        supplements: Dict,
        timing_rules: Dict,
        dosage_rules: Dict,
    ):
        self.analyzer = Analyzer(reference_ranges)
        self.rule_engine = RuleEngine(dosage_rules, supplements, timing_rules)

    def generate_recommendation(
        self, patient: Patient, blood_tests: List[BloodTest]
    ) -> Recommendation:
        analyzed_tests = self.analyzer.analyze_blood_tests(blood_tests)
        supplements_data = self.rule_engine.apply_rules(analyzed_tests, patient)

        supplement_recommendations = [
            SupplementRecommendation(
                name=supp["name"],
                dosage=supp["dosage"],
                timing=supp["timing"],
                priority=supp["priority"],
                reason=supp["reason"],
            )
            for supp in supplements_data
        ]

        supplement_recommendations.sort(key=self._priority_sort_key)

        return Recommendation(
            patient_name=patient.name,
            patient_surname=patient.surname,
            date=datetime.now(),
            supplements=supplement_recommendations,
        )

    def _priority_sort_key(self, supplement: SupplementRecommendation) -> int:
        return PRIORITY_ORDER.get(supplement.priority, 3)
