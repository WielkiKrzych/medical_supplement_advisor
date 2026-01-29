import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.utils.data_loader import DataLoader
from src.utils.validator import Validator
from src.utils.formatter import PDFFormatter
from src.utils.json_parser import JSONParser
from src.core.recommendation_engine import RecommendationEngine
from config import DATA_DIR, OUTPUT_DIR


def main():
    parser = argparse.ArgumentParser(
        description="Medical Supplement Advisor - Parser dokumentów JSON i generator rekomendacji"
    )
    parser.add_argument(
        "--json",
        type=str,
        help="Ścieżka do pojedynczego pliku JSON z danymi pacjenta i badaniami krwi",
    )
    parser.add_argument(
        "--patient",
        type=str,
        help="Ścieżka do pliku JSON z danymi pacjenta (oddzielny od badań)",
    )
    parser.add_argument(
        "--blood-tests",
        type=str,
        help="Ścieżka do pliku JSON z danymi badań krwi (oddzielny od pacjenta)",
    )
    args = parser.parse_args()

    if args.json:
        if args.patient or args.blood_tests:
            print("Błąd: Nie można używać --json razem z --patient lub --blood-tests")
            sys.exit(1)
    else:
        if not args.patient or not args.blood_tests:
            print("Błąd: Należy podać --json lub oba pliki: --patient i --blood-tests")
            print("Użycie:")
            print("  Opcja 1: --json <ścieżka_do_pliku.json>")
            print(
                "  Opcja 2: --patient <ścieżka_do_pliku_pacjenta.json> --blood-tests <ścieżka_do_pliku_badan.json>"
            )
            sys.exit(1)

    print("Medical Supplement Advisor")
    print("=" * 40)

    loader = DataLoader(DATA_DIR)

    reference_ranges = loader.load_reference_ranges()
    supplements = loader.load_supplements()
    timing_rules = loader.load_timing_rules()
    dosage_rules = loader.load_dosage_rules()

    json_parser = JSONParser()

    if args.json:
        parsed_data = json_parser.parse_document(Path(args.json))
        patient_data = parsed_data.get("patient")
        blood_tests_data = parsed_data.get("blood_tests")
    else:
        patient_parsed = json_parser.load_patient_only(Path(args.patient))
        blood_tests_parsed = json_parser.load_blood_tests_only(Path(args.blood_tests))
        patient_data = patient_parsed.get("patient")
        blood_tests_data = blood_tests_parsed.get("blood_tests")

    if not patient_data or not patient_data.get("name"):
        print("Błąd: Nie znaleziono danych pacjenta.")
        sys.exit(1)

    if not blood_tests_data:
        print("Błąd: Nie znaleziono badań krwi.")
        sys.exit(1)

    validator = Validator()

    patient = validator.validate_patient(patient_data)
    blood_tests = validator.validate_blood_tests(blood_tests_data)

    recommendation_engine = RecommendationEngine(
        reference_ranges=reference_ranges,
        supplements=supplements,
        timing_rules=timing_rules,
        dosage_rules=dosage_rules,
    )

    recommendation = recommendation_engine.generate_recommendation(patient, blood_tests)

    formatter = PDFFormatter(OUTPUT_DIR)
    pdf_path = formatter.generate_pdf(recommendation)

    print(f"\nWygenerowano raport: {pdf_path}")
    print(f"Liczba zarekomendowanych suplementów: {len(recommendation.supplements)}")

    if recommendation.supplements:
        print("\nZarekomendowane suplementy:")
        for supp in recommendation.supplements:
            print(f"  - {supp.name}: {supp.dosage} ({supp.priority})")


if __name__ == "__main__":
    main()
