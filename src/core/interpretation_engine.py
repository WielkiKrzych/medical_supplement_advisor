from typing import List, Dict, Any, Optional
from pathlib import Path
import json

from src.models.blood_test import BloodTest
from src.models.test_analysis import (
    TestAnalysis,
    Interpretation,
    ReferenceRange,
    MorphologyInterpretation,
    LipidInterpretation,
    ThyroidInterpretation,
    HormoneInterpretation,
    GlucoseInsulinInterpretation,
    LiverInterpretation,
    RatioAnalysis,
    CurveReading,
    GlucoseCurveAnalysis,
    InsulinCurveAnalysis,
)
from src.utils.data_loader import DataLoader
from config import DATA_DIR


class InterpretationEngine:
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_loader = DataLoader(data_dir)
        self.reference_data = self._load_reference_data()
        self.interpretation_rules = self._load_interpretation_rules()

    def _load_reference_data(self) -> Dict[str, Any]:
        try:
            return self.data_loader.load_json("reference_ranges_v2.json")
        except Exception:
            return {}

    def _load_interpretation_rules(self) -> Dict[str, Any]:
        try:
            return self.data_loader.load_json("interpretation_rules.json")
        except Exception:
            return {}

    def interpret_single_test(self, test: BloodTest) -> TestAnalysis:
        test_config = self._find_test_config(test.name)

        status = self._determine_status(test, test_config)
        interpretations = self._get_interpretations(test.name, status, test_config)
        deficiencies = self._identify_deficiencies(test.name, status, test_config)
        supplements = self._get_supplements(test.name, status)
        priority = self._determine_priority(test.name, status, test_config)

        return TestAnalysis(
            name=test.name,
            value=test.value,
            unit=test.unit,
            status=status,
            interpretations=interpretations,
            possible_deficiencies=deficiencies,
            recommended_supplements=supplements,
            priority=priority,
        )

    def _find_test_config(self, test_name: str) -> Optional[Dict]:
        if not self.reference_data:
            return None

        categories = self.reference_data.get("categories", {})
        for category_name, category_data in categories.items():
            tests = category_data.get("tests", [])
            for test in tests:
                if test.get("name", "").upper() == test_name.upper():
                    return test
        return None

    def _determine_status(self, test: BloodTest, config: Optional[Dict]) -> str:
        if not config:
            return "unknown"

        lab_ref = config.get("lab_reference", "")
        test_name = test.name.upper()
        value = test.value

        thresholds = {
            "TSH": (0.5, 2.5),
            "FERRYTYNA": (50, 90),
            "WITAMINA D3": (60, 80),
            "HOMOCYSTEINA": (5, 6),
            "HDL": (50, 100),
            "LDL": (100, 200),
            "TG": (60, 100),
            "AST": (10, 20),
            "ALT": (0, 26),
            "GGTP": (0, 26),
            "KORTYZOL": (0, 15),
            "PROLAKTYNA": (0, 25),
            "CRP": (0, 2),
            "NEUTROFILE": (40, 70),
            "MCV": (80, 100),
            "MCH": (27, 32),
        }

        if test_name in thresholds:
            low, high = thresholds[test_name]
            if value < low:
                return "low"
            elif value > high:
                return "high"
            return "normal"

        if "MAX" in lab_ref.upper():
            try:
                max_val = float(
                    lab_ref.upper().split("MAX")[1].split()[0].replace(",", ".")
                )
                if test.value > max_val:
                    return "high"
            except (ValueError, IndexError):
                pass

        return "normal"

    def _get_interpretations(
        self, test_name: str, status: str, config: Optional[Dict]
    ) -> List[Interpretation]:
        interpretations = []

        if not config:
            return interpretations

        key = f"{status.lower()}_interpretations"
        data = config.get(key, [])

        for interp_data in data:
            interpretations.append(
                Interpretation(
                    condition=status,
                    causes=interp_data.get("causes", []),
                    supplements=interp_data.get("supplements", []),
                    priority=interp_data.get("priority", "low"),
                    description=interp_data.get("interpretation", ""),
                )
            )

        return interpretations

    def _identify_deficiencies(
        self, test_name: str, status: str, config: Optional[Dict]
    ) -> List[str]:
        if not config or status != "low":
            return []

        key = "low_interpretations"
        data = config.get(key, [])

        deficiencies = []
        for interp in data:
            defs = interp.get("related_deficiencies", [])
            deficiencies.extend(defs)

        return list(set(deficiencies))

    def _get_supplements(self, test_name: str, status: str) -> List[str]:
        supplements = []

        rules = self.interpretation_rules.get("rules", {})
        single_rules = rules.get("single_test_rules", [])

        for rule in single_rules:
            if (
                rule.get("test_name", "").upper() == test_name.upper()
                and rule.get("condition") == status
            ):
                supplements.extend(rule.get("supplements", []))

        return list(set(supplements))

    def _determine_priority(
        self, test_name: str, status: str, config: Optional[Dict]
    ) -> str:
        if status == "normal":
            return "low"

        if not config:
            return "medium"

        key = f"{status.lower()}_interpretations"
        data = config.get(key, [])

        priorities = [interp.get("priority", "medium") for interp in data]

        if "critical" in priorities:
            return "critical"
        elif "high" in priorities:
            return "high"
        elif "medium" in priorities:
            return "medium"

        return "low"

    def interpret_morphology(self, tests: List[BloodTest]) -> MorphologyInterpretation:
        patterns = []
        deficiencies = []
        recommendations = []

        test_dict = {t.name.upper(): t for t in tests}

        if "MCV" in test_dict and "MCH" in test_dict:
            mcv = test_dict["MCV"].value
            mch = test_dict["MCH"].value

            if mcv < 80 and mch < 27:
                patterns.append("Mikrocytowa anemia (niedobór żelaza)")
                deficiencies.extend(["iron", "copper", "B6"])
                recommendations.extend(["Żelazo", "Miedź", "Witaminy z gr. B"])
            elif mcv > 100 and mch > 32:
                patterns.append("Megaloblastyczna anemia (niedobór B12/B9)")
                deficiencies.extend(["B12", "B9"])
                recommendations.extend(["B12", "Kwas foliowy"])

        if "NEUTROFILE" in test_dict:
            neut = test_dict["NEUTROFILE"]
            if neut.value < 40:
                patterns.append("Neutropenia - niedobór B12/B9")
                deficiencies.extend(["B12", "B9"])
                recommendations.extend(["Witaminy z gr. B", "L-Glutamina"])

        overall = "normal"
        if patterns:
            overall = "abnormal"

        return MorphologyInterpretation(
            overall_status=overall,
            patterns=patterns,
            deficiencies=list(set(deficiencies)),
            recommendations=list(set(recommendations)),
        )

    def interpret_lipid_profile(
        self, cholesterol: float, hdl: float, ldl: float, tg: float
    ) -> LipidInterpretation:
        ratios = []
        recommendations = []

        if hdl > 0 and ldl > 0:
            ratio = hdl / ldl
            ratio_analysis = RatioAnalysis(
                name="HDL:LDL",
                value=ratio,
                optimal_range="1:2",
                status="low" if ratio < 0.5 else "normal",
                interpretation="Niski stosunek - ryzyko sercowo-naczyniowe"
                if ratio < 0.5
                else "Prawidłowy",
                supplements=["Omega 3", "Omega 6", "Cholina"] if ratio < 0.5 else [],
            )
            ratios.append(ratio_analysis)

            if ratio < 0.5:
                recommendations.extend(["Omega 3", "Omega 6", "Cholina"])

        if hdl > 0 and tg > 0:
            ratio = hdl / tg
            status = "optimal" if ratio >= 1 else "low"
            ratios.append(
                RatioAnalysis(
                    name="HDL:TG",
                    value=ratio,
                    optimal_range="1:1",
                    status=status,
                    interpretation="Optymalny"
                    if status == "optimal"
                    else "Wymaga poprawy",
                    supplements=[] if status == "optimal" else ["Omega 3"],
                )
            )

        risk = "low"
        if ldl > 130 or tg > 100:
            risk = "moderate"
        if ldl > 160 or tg > 150:
            risk = "high"

        return LipidInterpretation(
            overall_status="abnormal" if risk != "low" else "normal",
            ratios=ratios,
            cardiovascular_risk=risk,
            recommendations=list(set(recommendations)),
        )

    def interpret_thyroid_panel(
        self, tsh: float, ft3: float, ft4: float, ft3_ref: tuple, ft4_ref: tuple
    ) -> ThyroidInterpretation:
        tsh_status = "normal"
        if tsh > 2.5:
            tsh_status = "high"
        elif tsh < 0.5:
            tsh_status = "low"

        ft3_pct = None
        ft4_pct = None

        if ft3_ref[1] > ft3_ref[0]:
            ft3_pct = ((ft3 - ft3_ref[0]) / (ft3_ref[1] - ft3_ref[0])) * 100

        if ft4_ref[1] > ft4_ref[0]:
            ft4_pct = ((ft4 - ft4_ref[0]) / (ft4_ref[1] - ft4_ref[0])) * 100

        recommendations = []

        if tsh_status == "high":
            recommendations.extend(["Selen", "Cynk", "Tyrozyna"])
        elif tsh_status == "low":
            recommendations.append("Koenzym Q10")

        if ft3_pct and ft3_pct < 50:
            recommendations.extend(["Selen", "Cynk", "Hepaset", "Maślan sodu"])

        overall = "normal"
        if tsh_status != "normal":
            overall = "abnormal"

        return ThyroidInterpretation(
            overall_status=overall,
            tsh_status=tsh_status,
            ft3_percentage=ft3_pct,
            ft4_percentage=ft4_pct,
            recommendations=list(set(recommendations)),
        )

    def analyze_glucose_curve(
        self, readings: List[Dict[str, Any]]
    ) -> GlucoseCurveAnalysis:
        curve_readings = []
        for r in readings:
            curve_readings.append(
                CurveReading(
                    timepoint=r.get("time", 0),
                    value=r.get("value", 0),
                    unit="mg/dL",
                    status=self._determine_glucose_status(
                        r.get("time", 0), r.get("value", 0)
                    ),
                )
            )

        fasting = readings[0]["value"] if readings else 0
        fasting_status = "normal"
        if fasting > 87:
            fasting_status = "high"
        elif fasting < 70:
            fasting_status = "low"

        peak_value = max(r.get("value", 0) for r in readings) if readings else 0
        peak_time = next(
            (r.get("time", 0) for r in readings if r.get("value", 0) == peak_value), 0
        )

        interpretations = []
        if fasting > 87:
            interpretations.append("Insulinooporność lub cukrzyca")

        return GlucoseCurveAnalysis(
            readings=curve_readings,
            fasting_status=fasting_status,
            peak_time=peak_time,
            peak_value=peak_value,
            interpretations=interpretations,
        )

    def _determine_glucose_status(self, time: int, value: float) -> str:
        optimal = {0: (70, 87), 60: (120, 140), 120: (0, 100), 180: (70, 90)}

        if time in optimal:
            min_v, max_v = optimal[time]
            if value < min_v:
                return "low"
            elif value > max_v:
                return "high"

        return "normal"

    def analyze_insulin_curve(
        self, readings: List[Dict[str, Any]]
    ) -> InsulinCurveAnalysis:
        curve_readings = []
        for r in readings:
            curve_readings.append(
                CurveReading(
                    timepoint=r.get("time", 0),
                    value=r.get("value", 0),
                    unit="uU/mL",
                    status=self._determine_insulin_status(
                        r.get("time", 0), r.get("value", 0)
                    ),
                )
            )

        fasting = readings[0]["value"] if readings else 0
        fasting_status = "normal"
        if fasting > 6:
            fasting_status = "high"
        elif fasting < 3:
            fasting_status = "low"

        interpretations = []
        if fasting > 6:
            interpretations.append("Insulinooporność")
        elif fasting < 3:
            interpretations.append("Możliwe hockiklocki w krzywej")

        return InsulinCurveAnalysis(
            readings=curve_readings,
            fasting_status=fasting_status,
            peak_time=60,
            peak_value=max(r.get("value", 0) for r in readings) if readings else 0,
            interpretations=interpretations,
        )

    def _determine_insulin_status(self, time: int, value: float) -> str:
        optimal = {0: (5, 6), 60: (0, 45), 120: (0, 30), 180: (0, 10)}

        if time in optimal:
            min_v, max_v = optimal[time]
            if value < min_v:
                return "low"
            elif value > max_v:
                return "high"

        return "normal"

    def calculate_ratio(
        self, name: str, value1: float, value2: float, optimal: str
    ) -> RatioAnalysis:
        if value2 == 0:
            value = 0
        else:
            value = value1 / value2

        status = "normal"
        interpretation = "Prawidłowy"
        supplements = []

        if name == "HDL:LDL":
            if value < 0.5:
                status = "low"
                interpretation = "Obciążona wątroba, stany zapalne"
                supplements = ["omega_3", "omega_6", "cholina"]

        elif name == "AST:ALT":
            if value > 2:
                status = "high"
                interpretation = "Uszkodzenie wątroby związane z alkoholem"
            elif value < 1:
                status = "low"
                interpretation = "Stłuszczenie wątroby lub insulinooporność"
                supplements = ["nac", "inozytol", "lactibiane_cnd", "ostropest"]

        elif name == "LH:FSH":
            if value > 2:
                status = "high"
                interpretation = "PCOS lub niewydolność jajników"
                supplements = ["myo-inozytol"]
            elif value < 0.5:
                status = "low"
                interpretation = "Niedoczynność przysadki"
                supplements = ["ashwagandha", "nac"]

        return RatioAnalysis(
            name=name,
            value=value,
            optimal_range=optimal,
            status=status,
            interpretation=interpretation,
            supplements=supplements,
        )

    def interpret_hormone_ratios(
        self, lh: float, fsh: float, e2: float, prog: float
    ) -> HormoneInterpretation:
        ratios = []

        if fsh > 0:
            ratio = self.calculate_ratio("LH:FSH", lh, fsh, "1:1")
            ratios.append(ratio)

        if prog > 0:
            ratio_val = e2 / prog
            status = "normal"
            supplements = []

            if ratio_val > 500:
                status = "high"
                supplements = ["dim", "inozytol", "nac"]
            elif ratio_val < 100:
                status = "low"
                supplements = ["ashwagandha"]

            ratios.append(
                RatioAnalysis(
                    name="Estradiol:Progesteron",
                    value=ratio_val,
                    optimal_range="100-500",
                    status=status,
                    interpretation="Dominacja estrogenowa"
                    if status == "high"
                    else "Niedobór estrogenów",
                    supplements=supplements,
                )
            )

        return HormoneInterpretation(
            overall_status="abnormal"
            if any(r.status != "normal" for r in ratios)
            else "normal",
            ratios=ratios,
            recommendations=[],
        )

    def interpret_liver_panel(
        self, ast: float, alt: float, ggtp: float
    ) -> LiverInterpretation:
        ratio = ast / alt if alt > 0 else 0

        pattern = None
        if ratio > 2:
            pattern = "alkoholowe uszkodzenie wątroby"
        elif ratio < 1 and ggtp > 35:
            pattern = "stłuszczenie wątroby lub insulinooporność"
        elif ast > 20 or alt > 26:
            pattern = "zapalenie wątroby"

        recommendations = []
        if pattern:
            recommendations.extend(["Hepaset", "Ostropest", "Liver Complex"])

        return LiverInterpretation(
            overall_status="abnormal" if pattern else "normal",
            ast_alt_ratio=ratio,
            pattern=pattern,
            recommendations=recommendations,
        )
