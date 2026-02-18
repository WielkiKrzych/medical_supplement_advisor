from src.models.blood_test import BloodTest
from typing import List, Dict, Literal


class Analyzer:
    """Analyzes blood test results against reference ranges.

    Determines if blood test values are low, normal, or high
    based on predefined reference ranges.
    """

    def __init__(self, reference_ranges: Dict):
        self.reference_ranges = reference_ranges["reference_ranges"]

    def analyze_blood_tests(self, blood_tests: List[BloodTest]) -> List[BloodTest]:
        analyzed_tests = []

        for test in blood_tests:
            ref_range = self._find_reference_range(test.name)

            if ref_range:
                status = self._determine_status(test.value, ref_range)
                test = test.model_copy(update={"status": status})

            analyzed_tests.append(test)

        return analyzed_tests

    def _find_reference_range(self, test_name: str) -> Dict | None:
        for ref_range in self.reference_ranges:
            if ref_range["name"] == test_name:
                return ref_range
        return None

    def _determine_status(
        self, value: float, ref_range: Dict
    ) -> Literal["low", "normal", "high"]:
        min_val = ref_range["min"]
        max_val = ref_range["max"]

        if value < min_val:
            return "low"
        elif value > max_val:
            return "high"
        else:
            return "normal"

    def get_abnormal_tests(self, blood_tests: List[BloodTest]) -> List[BloodTest]:
        return [test for test in blood_tests if test.status and test.status != "normal"]
