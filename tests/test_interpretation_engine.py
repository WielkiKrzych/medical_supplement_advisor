"""Tests for InterpretationEngine module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.models.blood_test import BloodTest
from src.core.interpretation_engine import InterpretationEngine
from config import DATA_DIR


@pytest.fixture
def interpretation_engine():
    return InterpretationEngine(DATA_DIR)


def test_interpret_single_test_low_value(interpretation_engine):
    """Test interpretation of a low blood test value."""
    test = BloodTest(name="WITAMINA D3", value=20.0, unit="ng/mL")
    analysis = interpretation_engine.interpret_single_test(test)

    assert analysis.name == "WITAMINA D3"
    assert analysis.value == 20.0
    assert analysis.status == "low"
    assert len(analysis.possible_deficiencies) > 0


def test_interpret_single_test_normal_value(interpretation_engine):
    """Test interpretation of a normal blood test value."""
    test = BloodTest(name="WITAMINA D3", value=65.0, unit="ng/mL")
    analysis = interpretation_engine.interpret_single_test(test)

    assert analysis.name == "WITAMINA D3"
    assert analysis.value == 65.0
    assert analysis.status == "normal"


def test_interpret_single_test_high_value(interpretation_engine):
    """Test interpretation of a high blood test value."""
    test = BloodTest(name="CRP", value=5.0, unit="mg/L")
    analysis = interpretation_engine.interpret_single_test(test)

    assert analysis.name == "CRP"
    assert analysis.value == 5.0
    assert analysis.status == "high"


def test_interpret_single_test_unknown_test(interpretation_engine):
    """Test interpretation of an unknown blood test."""
    test = BloodTest(name="UNKNOWN_TEST", value=50.0, unit="mg/dL")
    analysis = interpretation_engine.interpret_single_test(test)

    assert analysis.name == "UNKNOWN_TEST"
    assert analysis.value == 50.0
    assert analysis.status == "unknown"


def test_interpret_morphology_empty(interpretation_engine):
    """Test morphology interpretation with empty test list."""
    tests = []
    morphology = interpretation_engine.interpret_morphology(tests)

    assert morphology.overall_status == "normal"
    assert len(morphology.patterns) == 0
    assert len(morphology.deficiencies) == 0


def test_interpret_morphology_anemia_pattern(interpretation_engine):
    """Test morphology interpretation for anemia pattern."""
    tests = [
        BloodTest(name="MCV", value=75.0, unit="fL"),
        BloodTest(name="MCH", value=25.0, unit="pg"),
    ]
    morphology = interpretation_engine.interpret_morphology(tests)

    assert morphology.overall_status == "abnormal"
    assert len(morphology.patterns) > 0


def test_interpret_lipid_profile_normal(interpretation_engine):
    """Test lipid profile interpretation for normal values."""
    cholesterol = 180.0
    hdl = 55.0
    ldl = 110.0
    tg = 80.0

    lipids = interpretation_engine.interpret_lipid_profile(cholesterol, hdl, ldl, tg)

    assert lipids.overall_status == "normal"


def test_interpret_lipid_profile_high_risk(interpretation_engine):
    """Test lipid profile interpretation for high cardiovascular risk."""
    cholesterol = 250.0
    hdl = 35.0
    ldl = 170.0
    tg = 180.0

    lipids = interpretation_engine.interpret_lipid_profile(cholesterol, hdl, ldl, tg)

    assert lipids.overall_status == "abnormal"
    assert lipids.cardiovascular_risk == "high"


def test_interpret_thyroid_normal(interpretation_engine):
    """Test thyroid panel interpretation for normal values."""
    tsh = 1.5
    ft3 = 3.2
    ft4 = 1.3
    ft3_ref = (1.8, 4.6)
    ft4_ref = (0.93, 1.7)

    thyroid = interpretation_engine.interpret_thyroid_panel(tsh, ft3, ft4, ft3_ref, ft4_ref)

    assert thyroid.overall_status == "normal"
    assert thyroid.tsh_status == "normal"


def test_interpret_thyroid_hypothyroid(interpretation_engine):
    """Test thyroid panel interpretation for hypothyroidism."""
    tsh = 4.0
    ft3 = 3.2
    ft4 = 1.3
    ft3_ref = (1.8, 4.6)
    ft4_ref = (0.93, 1.7)

    thyroid = interpretation_engine.interpret_thyroid_panel(tsh, ft3, ft4, ft3_ref, ft4_ref)

    assert thyroid.overall_status == "abnormal"
    assert thyroid.tsh_status == "high"


def test_load_clinical_thresholds(interpretation_engine):
    """Test that clinical thresholds are loaded correctly."""
    assert len(interpretation_engine.clinical_thresholds) > 0

    # Check that TSH thresholds exist
    assert "TSH" in interpretation_engine.clinical_thresholds
    tsh_thresholds = interpretation_engine.clinical_thresholds["TSH"]
    assert "lab_min" in tsh_thresholds
    assert "lab_max" in tsh_thresholds
    assert "functional_min" in tsh_thresholds
    assert "functional_max" in tsh_thresholds
