import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
EXAMPLES_DIR = BASE_DIR / "examples"
OUTPUT_DIR = BASE_DIR / "output"

REFERENCE_RANGES_FILE = DATA_DIR / "reference_ranges.json"
SUPPLEMENTS_FILE = DATA_DIR / "supplements.json"
TIMING_RULES_FILE = DATA_DIR / "timing_rules.json"
DOSAGE_RULES_FILE = DATA_DIR / "dosage_rules.json"

SAMPLE_PATIENT_FILE = EXAMPLES_DIR / "sample_patient.json"
SAMPLE_BLOOD_TESTS_FILE = EXAMPLES_DIR / "sample_blood_tests.json"

OUTPUT_DIR.mkdir(exist_ok=True)

PRIORITY_CRITICAL = "critical"
PRIORITY_HIGH = "high"
PRIORITY_MEDIUM = "medium"
PRIORITY_LOW = "low"

PRIORITY_ORDER = {
    PRIORITY_CRITICAL: 0,
    PRIORITY_HIGH: 1,
    PRIORITY_MEDIUM: 2,
    PRIORITY_LOW: 3,
}

TIME_MORNING = "morning"
TIME_NOON = "noon"
TIME_EVENING = "evening"
TIME_NIGHT = "night"
TIME_WITH_MEAL = "with_meal"
TIME_BEFORE_MEAL = "before_meal"
TIME_ANY = "any"
