"""Tests for RecommendationEngine module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.models.patient import Patient
from src.models.blood_test import BloodTest
from src.core.analyzer import Analyzer
from src.core.recommendation_engine import RecommendationEngine
from config import PRIORITY_ORDER


@pytest.fixture
def reference_ranges():
    return {
        "reference_ranges": [
            {"name": "Witamina D (25-OH)", "min": 30.0, "max": 100.0, "unit": "ng/mL"},
            {"name": "Witamina B12", "min": 197.0, "max": 866.0, "unit": "pg/mL"},
        ]
    }


@pytest.fixture
def supplements():
    return {
        "supplements": [
            {"id": "vit_d3", "name": "Witamina D3"},
            {"id": "vit_b12", "name": "Witamina B12"},
            {"id": "iron", "name": "Żelazo"},
        ]
    }


@pytest.fixture
def timing_rules():
    return {
        "timing_rules": {"vit_d3": "with_meal", "vit_b12": "with_meal"},
        "timing_display": {"with_meal": "Z posiłkiem", "empty": "Dowolnie"},
    }


from typing import Any, Dict, cast


@pytest.fixture
def supplements():
    return {
        "supplements": [
            {
                "id": "vit_d3",
                "name": "Witamina D3",
                "condition": "niedobór witaminy D",
            },
            {
                "id": "vit_b12",
                "name": "Witamina B12",
                "condition": "niedobór witaminy B12",
            },
        ]
    }


@pytest.fixture
def timing_rules():
    return {
        "timing_rules": {"vit_d3": "with_meal", "vit_b12": "with_meal"},
        "timing_display": {"with_meal": "Z posiłkiem", "empty": "Dowolnie"},
    }


@pytest.fixture
def rules_data():
    return {
        "dosage_rules": [
            {
                "id": "vit_d_low",
                "condition_type": "single_test",
                "test_name": "Witamina D (25-OH)",
                "test_status": "low",
                "supplements": [
                    {
                        "supplement_id": "vit_d3",
                        "dosage": "2000 IU",
                        "priority": "critical",
                        "reason": "Niedobór witaminy D",
                    }
                ],
            }
        ]
    }


@pytest.fixture
def recommendation_engine(full_data):
    return RecommendationEngine(
        full_data["reference_ranges"],
        full_data["supplements"],
        full_data["timing_rules"],
        full_data["dosage_rules"],
    )


@pytest.fixture
def sample_patient():
    return Patient(name="Jan", surname="Kowalski", age=42, conditions=[])


@pytest.fixture
def analyzed_blood_tests():
    return [
        BloodTest(name="Witamina D (25-OH)", value=22.0, unit="ng/mL", status="low"),
        BloodTest(name="Witamina B12", value=150.0, unit="pg/mL", status="low"),
    ]


def test_recommendation_engine_generates_recommendation(
    recommendation_engine, sample_patient, analyzed_blood_tests
):
    """Test that recommendation engine generates recommendation."""
    recommendation = recommendation_engine.generate_recommendation(
        sample_patient, analyzed_blood_tests
    )

    assert recommendation is not None
    assert recommendation.patient_name == "Jan"
    assert recommendation.patient_surname == "Kowalski"
    assert len(recommendation.supplements) >= 1


def test_recommendation_engine_sorts_by_priority(recommendation_engine, sample_patient):
    """Test that recommendations are sorted by priority."""
    tests = [
        BloodTest(name="Witamina D (25-OH)", value=22.0, unit="ng/mL", status="low"),
        BloodTest(name="Witamina B12", value=150.0, unit="pg/mL", status="low"),
    ]
    recommendation = recommendation_engine.generate_recommendation(
        sample_patient, tests
    )

    assert len(recommendation.supplements) == 1


def test_recommendation_engine_high_priority_first(
    recommendation_engine, sample_patient
):
    """Test that critical priority supplements appear first."""
    tests = [
        BloodTest(name="Witamina D (25-OH)", value=22.0, unit="ng/mL", status="low")
    ]
    recommendation = recommendation_engine.generate_recommendation(
        sample_patient, tests
    )

    assert len(recommendation.supplements) > 0
    assert recommendation.supplements[0].priority == "critical"


def test_recommendation_engine_handles_empty_tests(
    recommendation_engine, sample_patient
):
    """Test that recommendation engine handles empty blood tests."""
    tests = []
    recommendation = recommendation_engine.generate_recommendation(
        sample_patient, tests
    )

    assert recommendation is not None
    assert len(recommendation.supplements) == 0


def test_recommendation_engine_includes_patient_conditions(
    recommendation_engine, full_data
):
    """Test that patient conditions are considered in recommendations."""
    rules = [
        {
            "id": "test_rule",
            "condition_type": "patient_condition",
            "condition": "inflammation",
            "supplements": [
                {
                    "supplement_id": "omega3",
                    "dosage": "1000 mg",
                    "priority": "medium",
                    "reason": "Stan zapalny",
                }
            ],
        }
    ]
    patient = Patient(
        name="Jan", surname="Kowalski", age=42, conditions=["inflammation"]
    )
    tests = [BloodTest(name="Test", value=50.0, unit="unit", status="normal")]

    recommendation = recommendation_engine.generate_recommendation(patient, tests)

    assert any("zapalny" in s.reason for s in recommendation.supplements)


def test_recommendation_engine_no_recommendations_for_normal_tests(
    recommendation_engine, sample_patient
):
    """Test that no recommendations are generated for normal blood tests."""
    tests = [BloodTest(name="Test", value=50.0, unit="ng/mL", status="normal")]
    recommendation = recommendation_engine.generate_recommendation(
        sample_patient, tests
    )

    assert recommendation is not None
    assert len(recommendation.supplements) == 0


def test_recommendation_engine_merges_duplicate_supplements(recommendation_engine):
    """Test that duplicate supplements are properly handled."""
    rules = [
        {
            "id": "rule1",
            "condition_type": "single_test",
            "test_name": "Test",
            "test_status": "low",
            "supplements": [
                {"supplement_id": "s1", "dosage": "10mg", "priority": "low"}
            ],
        },
        {
            "id": "rule2",
            "condition_type": "single_test",
            "test_name": "Test",
            "test_status": "low",
            "supplements": [
                {"supplement_id": "s1", "dosage": "20mg", "priority": "high"}
            ],
        },
    ]
    tests = [BloodTest(name="Test", value=10.0, unit="unit", status="low")]

    engine = RecommendationEngine({}, {}, rules, {})
    recommendation = engine.generate_recommendation(sample_patient, tests)

    # Higher priority should override lower priority
    assert len(recommendation.supplements) == 1
    assert recommendation.supplements[0].dosage == "20mg"
    assert recommendation.supplements[0].priority == "high"
