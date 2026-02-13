from typing import List, Dict, Any, Optional
from pathlib import Path

from src.models.blood_test import BloodTest
from src.models.patient import Patient
from src.models.test_analysis import (
    TestAnalysis,
    ComprehensiveAnalysis,
    SupplementRecommendation,
)
from src.core.interpretation_engine import InterpretationEngine
from src.utils.data_loader import DataLoader
from src.utils.i18n import t
from src.utils.logger import get_logger
from config import DATA_DIR

logger = get_logger(__name__)


class AdvancedAnalyzer:
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_loader = DataLoader(data_dir)
        self.interpretation_engine = InterpretationEngine(data_dir)
        self.supplements_data = self._load_supplements()
        self.test_categories = self._load_test_categories()

    def _load_test_categories(self) -> Dict[str, List[str]]:
        """Load test categories from JSON config file."""
        try:
            data = self.data_loader.load_json("test_categories.json")
            categories = data.get("categories", {})
            # Flatten categories into lookup dict: category -> list of test names (uppercase)
            return {
                cat_name: [t.upper() for t in cat_data.get("tests", [])]
                for cat_name, cat_data in categories.items()
            }
        except Exception as e:
            # Fallback to hardcoded lists if config fails to load
            logger.error(f"Failed to load test_categories.json: {e}")
            return {
                "morphology": [
                    "EOZYNOFILE", "LEUKOCYTY", "LIMFOCYTY", "NEUTROFILE",
                    "BAZOFILE", "MONOCYTY", "WBC", "HEMOGLOBINA",
                    "ERYTROCYTY", "HEMATOKRYT", "MCV", "MCH", "MCHC",
                    "RDW", "PDW", "PCT", "MPV"
                ],
                "inflammatory": ["CRP", "OB"],
                "minerals_vitamins": [
                    "ŻELAZO", "FERRYTYNA", "TRANSFERYNA", "WITAMINA B12",
                    "MMA", "WITAMINA B9", "WITAMINA D3", "HOMOCYSTEINA",
                    "CYNK", "SELEN", "FOSFATAZA ALKALICZNA", "CERULOPLAZMINA",
                    "PEROKSYDAZA GLUTATIONOWA", "JOD W MOCZU", "ENZYM DAO"
                ],
                "electrolytes": ["SÓD", "POTAS", "MAGNEZ", "FOSFOR"],
                "thyroid": ["TSH", "FT3", "FT4", "ANTY-TG", "ANTY-TPO", "TRAB"],
                "lipids": ["CHOLESTEROL", "HDL", "LDL", "TG", "TRÓGLICERYDY"],
                "liver": ["AST", "ALT", "GGTP"],
                "hormones": [
                    "TESTOSTERON", "DHT", "DHEAS", "ANDROSTENDION", "SHBG",
                    "PROGESTERON", "ESTRADIOL", "LH", "FSH", "PROLAKTYNA", "KORTYZOL"
                ],
                "glucose_insulin": ["GLUKOZA", "INSULINA", "HBA1C", "HOMA-IR"]
            }

    def _load_supplements(self) -> Dict[str, Any]:
        from src.utils.logger import get_logger
        logger = get_logger(__name__)
        try:
            data = self.data_loader.load_json("supplements_v2.json")
            supplements = {}
            for supp in data.get("supplements", []):
                supplements[supp["id"]] = supp
            logger.info(f"Loaded {len(supplements)} supplements from database")
            return supplements
        except Exception as e:
            logger.error(f"Failed to load supplements_v2.json: {e}")
            return {}

    def analyze_blood_tests(
        self, tests: List[BloodTest], patient: Patient
    ) -> ComprehensiveAnalysis:
        analyzed_tests = []
        for test in tests:
            analysis = self.interpretation_engine.interpret_single_test(test)
            analyzed_tests.append(analysis)

        morphology_tests = [t for t in tests if self._is_morphology_test(t.name)]
        morphology = self.interpretation_engine.interpret_morphology(morphology_tests)

        inflammatory = [
            a for a in analyzed_tests if self._is_inflammatory_marker(a.name)
        ]
        minerals = [a for a in analyzed_tests if self._is_mineral_vitamin(a.name)]
        electrolytes = [a for a in analyzed_tests if self._is_electrolyte(a.name)]

        thyroid = self._analyze_thyroid(tests)
        glucose_insulin = self._analyze_glucose_insulin(tests)
        lipids = self._analyze_lipids(tests)
        liver = self._analyze_liver(tests)
        hormones = self._analyze_hormones(tests)

        all_supplements = self._compile_supplements(
            analyzed_tests,
            morphology,
            thyroid,
            glucose_insulin,
            lipids,
            liver,
            hormones,
        )

        critical_issues = self._identify_critical_issues(
            analyzed_tests, morphology, thyroid, glucose_insulin, lipids, liver
        )

        return ComprehensiveAnalysis(
            patient_name=patient.name,
            patient_surname=patient.surname,
            morphology=morphology,
            inflammatory_markers=inflammatory,
            minerals_vitamins=minerals,
            electrolytes=electrolytes,
            thyroid=thyroid,
            glucose_insulin=glucose_insulin,
            lipids=lipids,
            liver=liver,
            hormones=hormones,
            all_supplements=all_supplements,
            critical_issues=critical_issues,
            recommendations_summary=self._generate_summary(
                critical_issues, all_supplements
            ),
        )

    def _is_morphology_test(self, name: str) -> bool:
        return name.upper() in self.test_categories.get("morphology", [])

    def _is_inflammatory_marker(self, name: str) -> bool:
        return name.upper() in self.test_categories.get("inflammatory", [])

    def _is_mineral_vitamin(self, name: str) -> bool:
        return name.upper() in self.test_categories.get("minerals_vitamins", [])

    def _is_electrolyte(self, name: str) -> bool:
        return name.upper() in self.test_categories.get("electrolytes", [])

    def _analyze_thyroid(self, tests: List[BloodTest]) -> Optional[Any]:
        test_dict = {t.name.upper(): t for t in tests}

        if "TSH" not in test_dict:
            return None

        tsh = test_dict["TSH"].value
        ft3 = test_dict.get("FT3", BloodTest(name="FT3", value=0, unit="pmol/L")).value
        ft4 = test_dict.get("FT4", BloodTest(name="FT4", value=0, unit="pmol/L")).value

        ft3_ref = (1.8, 4.6)
        ft4_ref = (0.93, 1.7)

        return self.interpretation_engine.interpret_thyroid_panel(
            tsh, ft3, ft4, ft3_ref, ft4_ref
        )

    def _analyze_glucose_insulin(self, tests: List[BloodTest]) -> Optional[Any]:
        test_dict = {t.name.upper(): t for t in tests}

        if "GLUKOZA" not in test_dict and "INSULINA" not in test_dict:
            return None

        glucose_readings = []
        insulin_readings = []

        for test in tests:
            if "GLUKOZA" in test.name.upper():
                time = self._extract_time(test.name)
                glucose_readings.append({"time": time, "value": test.value})
            elif "INSULINA" in test.name.upper():
                time = self._extract_time(test.name)
                insulin_readings.append({"time": time, "value": test.value})

        glucose_curve = None
        insulin_curve = None

        if glucose_readings:
            glucose_readings.sort(key=lambda x: x["time"])
            glucose_curve = self.interpretation_engine.analyze_glucose_curve(
                glucose_readings
            )

        if insulin_readings:
            insulin_readings.sort(key=lambda x: x["time"])
            insulin_curve = self.interpretation_engine.analyze_insulin_curve(
                insulin_readings
            )

        homa_ir = None
        if "GLUKOZA" in test_dict and "INSULINA" in test_dict:
            glucose_0 = test_dict["GLUKOZA"].value
            insulin_0 = test_dict["INSULINA"].value
            homa_ir = (glucose_0 * insulin_0) / 405

        hba1c_status = None
        if "HBA1C" in test_dict:
            hba1c = test_dict["HBA1C"].value
            if 4.8 <= hba1c <= 5.2:
                hba1c_status = "optimal"
            elif hba1c < 4.8:
                hba1c_status = "low"
            else:
                hba1c_status = "high"

        insulin_resistance = False
        if homa_ir and homa_ir > 1.5:
            insulin_resistance = True

        recommendations = []
        if insulin_resistance:
            recommendations.extend(["NAC", "Inozytol", "Berberyna", "Lactibiane CND"])

        from src.models.test_analysis import GlucoseInsulinInterpretation

        return GlucoseInsulinInterpretation(
            overall_status="abnormal" if insulin_resistance else "normal",
            insulin_resistance=insulin_resistance,
            glucose_curve=glucose_curve,
            insulin_curve=insulin_curve,
            homa_ir=homa_ir,
            hba1c_status=hba1c_status,
            recommendations=recommendations,
        )

    def _extract_time(self, name: str) -> int:
        name_upper = name.upper()
        if "CZCO" in name_upper or "0H" in name_upper:
            return 0
        elif "1H" in name_upper or "60" in name_upper:
            return 60
        elif "2H" in name_upper or "120" in name_upper:
            return 120
        elif "3H" in name_upper or "180" in name_upper:
            return 180
        return 0

    def _analyze_lipids(self, tests: List[BloodTest]) -> Optional[Any]:
        test_dict = {t.name.upper(): t for t in tests}

        cholesterol = test_dict.get(
            "CHOLESTEROL", BloodTest(name="Cholesterol", value=0, unit="mg/dL")
        ).value
        hdl = test_dict.get("HDL", BloodTest(name="HDL", value=0, unit="mg/dL")).value
        ldl = test_dict.get("LDL", BloodTest(name="LDL", value=0, unit="mg/dL")).value
        tg = test_dict.get("TG", BloodTest(name="TG", value=0, unit="mg/dL")).value

        if cholesterol == 0 and hdl == 0 and ldl == 0 and tg == 0:
            return None

        return self.interpretation_engine.interpret_lipid_profile(
            cholesterol, hdl, ldl, tg
        )

    def _analyze_liver(self, tests: List[BloodTest]) -> Optional[Any]:
        test_dict = {t.name.upper(): t for t in tests}

        ast = test_dict.get("AST", BloodTest(name="AST", value=0, unit="U/L")).value
        alt = test_dict.get("ALT", BloodTest(name="ALT", value=0, unit="U/L")).value
        ggtp = test_dict.get("GGTP", BloodTest(name="GGTP", value=0, unit="U/L")).value

        if ast == 0 and alt == 0 and ggtp == 0:
            return None

        return self.interpretation_engine.interpret_liver_panel(ast, alt, ggtp)

    def _analyze_hormones(self, tests: List[BloodTest]) -> Optional[Any]:
        test_dict = {t.name.upper(): t for t in tests}

        lh = test_dict.get("LH", BloodTest(name="LH", value=0, unit="IU/L")).value
        fsh = test_dict.get("FSH", BloodTest(name="FSH", value=0, unit="IU/L")).value
        e2 = test_dict.get(
            "ESTRADIOL", BloodTest(name="Estradiol", value=0, unit="pg/mL")
        ).value
        prog = test_dict.get(
            "PROGESTERON", BloodTest(name="Progesteron", value=0, unit="ng/mL")
        ).value

        if lh == 0 and fsh == 0 and e2 == 0 and prog == 0:
            return None

        return self.interpretation_engine.interpret_hormone_ratios(lh, fsh, e2, prog)

    def _compile_supplements(
        self,
        analyzed_tests: List[TestAnalysis],
        morphology: Any,
        thyroid: Any,
        glucose_insulin: Any,
        lipids: Any,
        liver: Any,
        hormones: Any,
    ) -> List[SupplementRecommendation]:
        supplement_ids = set()

        for test in analyzed_tests:
            supplement_ids.update(test.recommended_supplements)

        if morphology:
            for rec in morphology.recommendations:
                supplement_ids.add(rec.lower().replace(" ", "_"))

        if thyroid:
            for rec in thyroid.recommendations:
                supplement_ids.add(rec.lower().replace(" ", "_"))

        if glucose_insulin:
            for rec in glucose_insulin.recommendations:
                supplement_ids.add(rec.lower().replace(" ", "_"))

        recommendations = []
        for supp_id in supplement_ids:
            supp_data = self.supplements_data.get(supp_id)
            if supp_data:
                recommendations.append(
                    SupplementRecommendation(
                        supplement_id=supp_id,
                        name=supp_data["name"],
                        dosage=supp_data["dosage"],
                        priority="high",
                        reason=f"Wskazane dla {supp_data['category']}",
                        contraindications=supp_data.get("contraindications", []),
                        interactions=supp_data.get("interactions", []),
                    )
                )

        return sorted(recommendations, key=lambda x: x.priority)

    def _identify_critical_issues(
        self,
        analyzed_tests: List[TestAnalysis],
        morphology: Any,
        thyroid: Any,
        glucose_insulin: Any,
        lipids: Any,
        liver: Any,
    ) -> List[str]:
        issues = []

        for test in analyzed_tests:
            if test.priority == "critical":
                issues.append(f"{test.name}: {test.status}")

        if morphology and morphology.deficiencies:
            for defic in morphology.deficiencies:
                issues.append(f"{t('analysis.deficiency')}: {defic}")

        if thyroid and thyroid.tsh_status != "normal":
            issues.append(t("analysis.thyroid_abnormal"))

        if glucose_insulin and glucose_insulin.insulin_resistance:
            issues.append(t("analysis.insulin_resistance"))

        if lipids and lipids.cardiovascular_risk == "high":
            issues.append(t("analysis.cardiovascular_risk_high"))

        if liver and liver.pattern:
            issues.append(f"{t('categories.liver')}: {liver.pattern}")

        return issues

    def _generate_summary(
        self, critical_issues: List[str], supplements: List[SupplementRecommendation]
    ) -> List[str]:
        summary = []

        if critical_issues:
            summary.append(t("analysis.critical_issues_found", len(critical_issues)))

        if supplements:
            summary.append(t("analysis.supplements_recommended", len(supplements)))

        return summary
