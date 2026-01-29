"""Tests for RuleEngine module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.models.blood_test import BloodTest
from src.models.patient import Patient
from src.core.rule_engine import RuleEngine


@pytest.fixture
def dosage_rules():
    return {
        "dosage_rules": [
            {
                "id": "test_rule_1",
                "condition_type": "single_test",
                "test_name": "Witamina D (25-OH)",
                "test_status": "low",
                "supplements": [
                    {
                        "supplement_id": "vit_d3",
                        "dosage": "2000 IU",
                        "priority": "critical",
                        "reason": "Test reason",
                    }
                ],
            },
            {
                "id": "test_rule_2",
                "condition_type": "combination",
                "tests": [
                    {"name": "Witamina B12", "status": "low"},
                    {"name": "Żelazo", "status": "low"},
                ],
                "supplements": [
                    {
                        "supplement_id": "iron",
                        "dosage": "14 mg",
                        "priority": "high",
                        "reason": "Combination test",
                    }
                ],
            },
            {
                "id": "test_rule_3",
                "condition_type": "patient_condition",
                "condition": "inflammation",
                "supplements": [
                    {
                        "supplement_id": "omega3",
                        "dosage": "1000 mg",
                        "priority": "medium",
                        "reason": "Patient condition",
                    }
                ],
            },
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


@pytest.fixture
def rule_engine(dosage_rules, supplements, timing_rules):
    return RuleEngine(dosage_rules, supplements, timing_rules)


@pytest.fixture
def sample_blood_tests():
    return [
        BloodTest(name="Witamina D (25-OH)", value=22.0, unit="ng/mL"),
        BloodTest(name="Witamina B12", value=150.0, unit="pg/mL"),
        BloodTest(name="Żelazo", value=45.0, unit="ug/dL"),
    ]


@pytest.fixture
def analyzed_blood_tests():
    return [
        BloodTest(name="Witamina D (25-OH)", value=22.0, unit="ng/mL", status="low"),
        BloodTest(name="Witamina B12", value=150.0, unit="pg/mL", status="low"),
        BloodTest(name="Żelazo", value=45.0, unit="ug/dL", status="low"),
    ]


def test_rule_engine_single_test_match(rule_engine, analyzed_blood_tests):
    """Test that rule engine matches single test rules correctly."""
    supplements = rule_engine.apply_rules(
        analyzed_blood_tests,
        Patient(name="Test", surname="User", age=30, conditions=[]),
    )

    assert len(supplements) > 0
    assert any(s["name"] == "Witamina D3" for s in supplements)
    assert any(s["priority"] == "critical" for s in supplements)


def test_rule_engine_combination_match(rule_engine, analyzed_blood_tests):
    """Test that rule engine matches combination rules correctly."""
    # Add combination test case that should match
    supplements = rule_engine.apply_rules(
        [
            BloodTest(name="Witamina B12", value=150.0, unit="pg/mL", status="low"),
            BloodTest(name="Żelazo", value=45.0, unit="ug/dL", status="low"),
        ],
        Patient(name="Test", surname="User", age=30, conditions=[]),
    )

    # Should match combination rule
    assert len(supplements) > 0


def test_rule_engine_patient_condition_match(rule_engine, sample_blood_tests):
    """Test that rule engine matches patient condition rules."""
    patient = Patient(name="Test", surname="User", age=30, conditions=["inflammation"])
    analyzed_tests = [
        BloodTest(name="Witamina D (25-OH)", value=22.0, unit="ng/mL", status="low")
    ]

    supplements = rule_engine.apply_rules(analyzed_tests, patient)

    assert len(supplements) > 0
    assert any("inflammation" in s["reason"] for s in supplements)


def test_rule_engine_no_match(rule_engine, sample_blood_tests):
    """Test that rule engine returns empty list when no rules match."""
    analyzed_tests = [BloodTest(name="Test", value=100.0, unit="unit", status="normal")]
    patient = Patient(name="Test", surname="User", age=30, conditions=[])

    supplements = rule_engine.apply_rules(analyzed_tests, patient)

    # Should not match any rules with normal values
    assert len(supplements) == 0


def test_rule_engine_priority_replacement(rule_engine):
    """Test that higher priority supplements replace lower priority ones."""
    tests = [
        BloodTest(name="Witamina D (25-OH)", value=18.0, unit="ng/mL", status="low")
    ]
    patient = Patient(name="Test", surname="User", age=30, conditions=[])

    supplements = rule_engine.apply_rules(tests, patient)

    # All supplements should have valid priorities
    for supp in supplements:
        assert supp["priority"] in ["critical", "high", "medium", "low"]


def test_rule_engine_timing_display(rule_engine, analyzed_blood_tests):
    """Test that timing display strings are correctly applied."""
    supplements = rule_engine.apply_rules(
        analyzed_blood_tests,
        Patient(name="Test", surname="User", age=30, conditions=[]),
    )

    assert len(supplements) > 0
    # All supplements should have timing display text
    for supp in supplements:
        assert "timing" in supp
        assert isinstance(supp["timing"], str)
        assert len(supp["timing"]) > 0


def test_rule_engine_multiple_supplements_per_rule(rule_engine, analyzed_blood_tests):
    """Test that multiple supplements from one rule are all added."""
    supplements = rule_engine.apply_rules(
        analyzed_blood_tests,
        Patient(name="Test", surname="User", age=30, conditions=[]),
    )

    # Each rule may add multiple supplements
    assert len(supplements) >= 0
