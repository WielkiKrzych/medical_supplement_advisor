import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.models.blood_test import BloodTest
from src.models.patient import Patient
from src.core.advanced_analyzer import AdvancedAnalyzer
from src.core.interpretation_engine import InterpretationEngine


@pytest.fixture
def sample_patient():
    return Patient(name="Jan", surname="Kowalski", age=35, conditions=[])


@pytest.fixture
def advanced_analyzer():
    return AdvancedAnalyzer()


@pytest.fixture
def interpretation_engine():
    return InterpretationEngine()


class TestInterpretationEngine:
    def test_interpret_single_test_neutrophils_low(self, interpretation_engine):
        test = BloodTest(name="NEUTROFILE", value=35, unit="%")
        result = interpretation_engine.interpret_single_test(test)

        assert result.name == "NEUTROFILE"
        assert result.status == "low"
        assert len(result.interpretations) > 0
        assert result.priority == "high"

    def test_interpret_single_test_tsh_high(self, interpretation_engine):
        test = BloodTest(name="TSH", value=3.5, unit="mIU/L")
        result = interpretation_engine.interpret_single_test(test)

        assert result.name == "TSH"
        assert result.status == "high"
        assert "selen" in [
            s.lower() for s in result.recommended_supplements
        ] or "cynk" in [s.lower() for s in result.recommended_supplements]

    def test_interpret_single_test_ferritin_low(self, interpretation_engine):
        test = BloodTest(name="FERRYTYNA", value=30, unit="ng/mL")
        result = interpretation_engine.interpret_single_test(test)

        assert result.name == "FERRYTYNA"
        assert result.status == "low"
        assert result.priority == "high"

    def test_interpret_morphology_iron_deficiency(self, interpretation_engine):
        tests = [
            BloodTest(name="MCV", value=75, unit="fL"),
            BloodTest(name="MCH", value=25, unit="pg"),
        ]
        result = interpretation_engine.interpret_morphology(tests)

        assert result.overall_status == "abnormal"
        assert any("żelaza" in p.lower() for p in result.patterns)
        assert "iron" in result.deficiencies

    def test_interpret_morphology_b12_deficiency(self, interpretation_engine):
        tests = [
            BloodTest(name="MCV", value=105, unit="fL"),
            BloodTest(name="MCH", value=34, unit="pg"),
        ]
        result = interpretation_engine.interpret_morphology(tests)

        assert result.overall_status == "abnormal"
        assert any("b12" in p.lower() or "b9" in p.lower() for p in result.patterns)

    def test_interpret_lipid_profile_high_risk(self, interpretation_engine):
        result = interpretation_engine.interpret_lipid_profile(
            cholesterol=240, hdl=40, ldl=160, tg=150
        )

        assert result.overall_status == "abnormal"
        assert result.cardiovascular_risk in ["high", "moderate"]
        assert len(result.ratios) > 0

    def test_interpret_thyroid_hypothyroidism(self, interpretation_engine):
        result = interpretation_engine.interpret_thyroid_panel(
            tsh=3.5, ft3=3.0, ft4=1.0, ft3_ref=(1.8, 4.6), ft4_ref=(0.93, 1.7)
        )

        assert result.tsh_status == "high"
        assert result.overall_status == "abnormal"
        assert any("selen" in r.lower() for r in result.recommendations)

    def test_calculate_ratio_hdl_ldl_low(self, interpretation_engine):
        result = interpretation_engine.calculate_ratio("HDL:LDL", 40, 120, "1:2")

        assert result.name == "HDL:LDL"
        assert result.status == "low"
        assert len(result.supplements) > 0

    def test_calculate_ratio_ast_alt_fatty_liver(self, interpretation_engine):
        result = interpretation_engine.calculate_ratio("AST:ALT", 20, 35, "Do 2")

        assert result.name == "AST:ALT"
        assert result.status == "low"
        assert "stłuszczenie" in result.interpretation.lower()

    def test_calculate_ratio_lh_fsh_pcos(self, interpretation_engine):
        result = interpretation_engine.calculate_ratio("LH:FSH", 15, 6, "1:1")

        assert result.name == "LH:FSH"
        assert result.status == "high"
        assert "pcos" in result.interpretation.lower()


class TestAdvancedAnalyzer:
    def test_analyze_blood_tests_comprehensive(self, advanced_analyzer, sample_patient):
        tests = [
            BloodTest(name="NEUTROFILE", value=35, unit="%"),
            BloodTest(name="TSH", value=3.5, unit="mIU/L"),
            BloodTest(name="FERRYTYNA", value=30, unit="ng/mL"),
            BloodTest(name="HDL", value=40, unit="mg/dL"),
            BloodTest(name="LDL", value=160, unit="mg/dL"),
        ]

        result = advanced_analyzer.analyze_blood_tests(tests, sample_patient)

        assert result.patient_name == "Jan"
        assert result.patient_surname == "Kowalski"
        assert result.morphology is not None
        assert result.thyroid is not None
        assert len(result.critical_issues) > 0
        assert len(result.all_supplements) > 0

    def test_analyze_glucose_insulin_resistance(
        self, advanced_analyzer, sample_patient
    ):
        tests = [
            BloodTest(name="GLUKOZA", value=95, unit="mg/dL"),
            BloodTest(name="INSULINA", value=15, unit="uU/mL"),
        ]

        result = advanced_analyzer.analyze_blood_tests(tests, sample_patient)

        if result.glucose_insulin:
            assert result.glucose_insulin.insulin_resistance == True
            assert result.glucose_insulin.homa_ir > 1.5

    def test_analyze_liver_panel(self, advanced_analyzer, sample_patient):
        tests = [
            BloodTest(name="AST", value=25, unit="U/L"),
            BloodTest(name="ALT", value=45, unit="U/L"),
            BloodTest(name="GGTP", value=50, unit="U/L"),
        ]

        result = advanced_analyzer.analyze_blood_tests(tests, sample_patient)

        if result.liver:
            assert result.liver.overall_status == "abnormal"
            assert result.liver.pattern is not None

    def test_critical_issues_identification(self, advanced_analyzer, sample_patient):
        tests = [
            BloodTest(name="TSH", value=5.0, unit="mIU/L"),
            BloodTest(name="FERRYTYNA", value=20, unit="ng/mL"),
            BloodTest(name="HBA1C", value=6.5, unit="%"),
        ]

        result = advanced_analyzer.analyze_blood_tests(tests, sample_patient)

        assert len(result.critical_issues) >= 1
        assert any("tsh" in issue.lower() for issue in result.critical_issues)


class TestCurveAnalysis:
    def test_analyze_glucose_curve_normal(self, interpretation_engine):
        readings = [
            {"time": 0, "value": 80},
            {"time": 60, "value": 130},
            {"time": 120, "value": 95},
            {"time": 180, "value": 85},
        ]

        result = interpretation_engine.analyze_glucose_curve(readings)

        assert result.fasting_status == "normal"
        assert result.peak_value == 130
        assert len(result.readings) == 4

    def test_analyze_glucose_curve_high_fasting(self, interpretation_engine):
        readings = [
            {"time": 0, "value": 95},
            {"time": 60, "value": 150},
        ]

        result = interpretation_engine.analyze_glucose_curve(readings)

        assert result.fasting_status == "high"
        assert len(result.interpretations) > 0

    def test_analyze_insulin_curve_resistance(self, interpretation_engine):
        readings = [
            {"time": 0, "value": 12},
            {"time": 60, "value": 80},
            {"time": 120, "value": 50},
        ]

        result = interpretation_engine.analyze_insulin_curve(readings)

        assert result.fasting_status == "high"
        assert len(result.interpretations) > 0
        assert "insulinooporność" in result.interpretations[0].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
