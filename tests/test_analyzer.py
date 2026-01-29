"""Tests for Analyzer module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.models.blood_test import BloodTest
from src.core.analyzer import Analyzer


@pytest.fixture
def reference_ranges():
    return {
        "reference_ranges": [
            {"name": "Witamina D (25-OH)", "min": 30.0, "max": 100.0, "unit": "ng/mL"},
            {"name": "Witamina B12", "min": 197.0, "max": 866.0, "unit": "pg/mL"},
            {"name": "Żelazo", "min": 60.0, "max": 170.0, "unit": "ug/dL"},
        ]
    }


@pytest.fixture
def analyzer(reference_ranges):
    return Analyzer(reference_ranges)


@pytest.fixture
def sample_blood_tests():
    return [
        BloodTest(name="Witamina D (25-OH)", value=22.0, unit="ng/mL"),
        BloodTest(name="Witamina B12", value=150.0, unit="pg/mL"),
        BloodTest(name="Żelazo", value=45.0, unit="ug/dL"),
        BloodTest(name="Magnez (Mg)", value=1.5, unit="mg/dL"),
    ]


def test_analyzer_determines_low_status(analyzer, sample_blood_tests):
    """Test that analyzer correctly identifies low values."""
    analyzed = analyzer.analyze_blood_tests(sample_blood_tests[:1])

    assert len(analyzed) == 1
    assert analyzed[0].status == "low"
    assert analyzed[0].name == "Witamina D (25-OH)"


def test_analyzer_determines_high_status(analyzer, sample_blood_tests):
    """Test that analyzer correctly identifies high values."""
    tests = [
        BloodTest(name="Witamina B12", value=1200.0, unit="pg/mL"),
        BloodTest(name="Żelazo", value=300.0, unit="ug/dL"),
    ]
    analyzed = analyzer.analyze_blood_tests(tests)

    assert len(analyzed) == 2
    assert all(t.status == "high" for t in analyzed)


def test_analyzer_determines_normal_status(analyzer, sample_blood_tests):
    """Test that analyzer correctly identifies normal values."""
    tests = [
        BloodTest(name="Witamina D (25-OH)", value=50.0, unit="ng/mL"),
        BloodTest(name="Witamina B12", value=400.0, unit="pg/mL"),
    ]
    analyzed = analyzer.analyze_blood_tests(tests)

    assert len(analyzed) == 2
    assert all(t.status == "normal" for t in analyzed)


def test_analyzer_preserves_status_for_unknown_tests(analyzer):
    """Test that analyzer preserves original status for tests without reference range."""
    tests = [
        BloodTest(name="Unknown Test", value=50.0, unit="unit"),
    ]
    analyzed = analyzer.analyze_blood_tests(tests)

    assert len(analyzed) == 1
    assert analyzed[0].status is None


def test_analyzer_get_abnormal_tests(analyzer):
    """Test that analyzer correctly filters abnormal tests."""
    tests = [
        BloodTest(name="Witamina D (25-OH)", value=22.0, unit="ng/mL", status="low"),
        BloodTest(name="Witamina B12", value=150.0, unit="pg/mL", status="low"),
        BloodTest(name="Magnez (Mg)", value=1.5, unit="mg/dL", status="normal"),
        BloodTest(name="Żelazo", value=45.0, unit="ug/dL", status="low"),
    ]
    analyzed = analyzer.analyze_blood_tests(tests)
    abnormal = analyzer.get_abnormal_tests(analyzed)

    assert len(abnormal) == 3
    assert all(t.status == "low" for t in abnormal)


def test_analyzer_handles_empty_list(analyzer):
    """Test that analyzer handles empty blood test list."""
    analyzed = analyzer.analyze_blood_tests([])

    assert len(analyzed) == 0


def test_analyzer_value_range_lower_than_min(analyzer):
    """Test that analyzer correctly identifies values below minimum."""
    tests = [BloodTest(name="Witamina D (25-OH)", value=20.0, unit="ng/mL")]
    analyzed = analyzer.analyze_blood_tests(tests)

    assert len(analyzed) == 1
    assert analyzed[0].status == "low"


def test_analyzer_value_range_higher_than_max(analyzer):
    """Test that analyzer correctly identifies values above maximum."""
    tests = [BloodTest(name="Witamina D (25-OH)", value=110.0, unit="ng/mL")]
    analyzed = analyzer.analyze_blood_tests(tests)

    assert len(analyzed) == 1
    assert analyzed[0].status == "high"
