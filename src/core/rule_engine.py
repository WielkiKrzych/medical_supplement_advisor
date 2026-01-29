from src.models.blood_test import BloodTest
from src.models.patient import Patient
from typing import List, Dict
from config import PRIORITY_ORDER


class RuleEngine:
    """Engine for applying dosage and timing rules to blood test results.

    Matches blood tests and patient conditions against configured rules
    to determine appropriate supplements, dosages, and timing.
    """

    def __init__(self, dosage_rules: Dict, supplements: Dict, timing_rules: Dict):
        self.dosage_rules = dosage_rules["dosage_rules"]
        self.supplements = {s["id"]: s for s in supplements["supplements"]}
        self.timing_rules = timing_rules["timing_rules"]
        self.timing_display = timing_rules["timing_display"]

    def apply_rules(self, blood_tests: List[BloodTest], patient: Patient) -> List[Dict]:
        matched_supplements = {}

        for rule in self.dosage_rules:
            if self._matches_rule(rule, blood_tests, patient):
                for supplement_rule in rule["supplements"]:
                    supplement_id = supplement_rule["supplement_id"]

                    if supplement_id in self.supplements:
                        supplement_info = self.supplements[supplement_id]
                        timing_key = self.timing_rules.get(supplement_id, "with_meal")
                        timing_display = self.timing_display.get(
                            timing_key, "Z posiłkiem"
                        )

                        supplement_data = {
                            "name": supplement_info["name"],
                            "dosage": supplement_rule["dosage"],
                            "timing": timing_display,
                            "priority": supplement_rule["priority"],
                            "reason": supplement_rule["reason"],
                        }

                        supplement_key = (
                            f"{supplement_info['name']}_{supplement_rule['dosage']}"
                        )

                        if supplement_key not in matched_supplements:
                            matched_supplements[supplement_key] = supplement_data
                        elif self._should_replace(
                            matched_supplements[supplement_key], supplement_data
                        ):
                            matched_supplements[supplement_key] = supplement_data

        return list(matched_supplements.values())

    def _matches_rule(
        self, rule: Dict, blood_tests: List[BloodTest], patient: Patient
    ) -> bool:
        condition_type = rule["condition_type"]

        if condition_type == "single_test":
            return self._matches_single_test_rule(rule, blood_tests)
        elif condition_type == "combination":
            return self._matches_combination_rule(rule, blood_tests)
        elif condition_type == "patient_condition":
            return self._matches_patient_condition_rule(rule, patient)

        return False

    def _matches_single_test_rule(
        self, rule: Dict, blood_tests: List[BloodTest]
    ) -> bool:
        test_name = rule["test_name"]
        test = self._find_blood_test_by_name(blood_tests, test_name)

        if not test or not test.status:
            return False

        if rule.get("test_status") and test.status != rule["test_status"]:
            return False

        if "test_value_range" in rule:
            value_range = rule["test_value_range"]
            if "min" in value_range and test.value < value_range["min"]:
                return False
            if "max" in value_range and test.value > value_range["max"]:
                return False

        return True

    def _matches_combination_rule(
        self, rule: Dict, blood_tests: List[BloodTest]
    ) -> bool:
        required_tests = rule.get("tests", [])

        for required_test in required_tests:
            test = self._find_blood_test_by_name(blood_tests, required_test["name"])
            if not test:
                return False
            if not test.status or test.status != required_test["status"]:
                return False

        return True

    def _matches_patient_condition_rule(self, rule: Dict, patient: Patient) -> bool:
        required_condition = rule["condition"]
        return required_condition in patient.conditions

    def _find_blood_test_by_name(
        self, blood_tests: List[BloodTest], name: str
    ) -> BloodTest | None:
        for test in blood_tests:
            if test.name == name:
                return test
        return None

    def _should_replace(self, existing: Dict, new: Dict) -> bool:
        return PRIORITY_ORDER.get(new["priority"], 4) < PRIORITY_ORDER.get(
            existing["priority"], 4
        )
