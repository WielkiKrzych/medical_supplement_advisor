import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.utils.data_loader import DataLoader
from src.utils.validator import Validator
from src.utils.formatter import PDFFormatter
from src.utils.json_parser import JSONParser
from src.utils.document_parser import DocumentParser
from src.core.recommendation_engine import RecommendationEngine
from config import DATA_DIR, OUTPUT_DIR


def run_web(patient, blood_tests, host="127.0.0.1", port=8000, no_browser=False):
    import threading
    import webbrowser

    import uvicorn

    from src.core.advanced_analyzer import AdvancedAnalyzer
    from src.web.app import create_app

    analyzer = AdvancedAnalyzer()
    comprehensive = analyzer.analyze_blood_tests(blood_tests, patient)
    app = create_app(analysis=comprehensive)

    if not no_browser:
        url = f"http://{host}:{port}"
        threading.Timer(1.5, lambda: webbrowser.open(url)).start()

    print(f"\n🌐 Serwer uruchomiony: http://{host}:{port}")
    print("Naciśnij Ctrl+C aby zatrzymać\n")
    uvicorn.run(app, host=host, port=port)


def run_cli():
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
    parser.add_argument(
        "--document",
        type=str,
        help="Ścieżka do pliku PDF lub DOCX z wynikami badań (automatyczne parsowanie)",
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Uruchom interaktywny dashboard webowy",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host serwera webowego",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port serwera webowego",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Nie otwieraj automatycznie przeglądarki",
    )
    args = parser.parse_args()

    has_args = any([args.json, args.patient, args.blood_tests, args.document, args.web])

    if not has_args:
        return False  # No CLI arguments, should run GUI instead

    # Process CLI arguments
    if args.document:
        if args.patient or args.blood_tests or args.json:
            print(
                "Błąd: Nie można używać --document razem z --json, --patient lub --blood-tests"
            )
            sys.exit(1)

        # Parse document (PDF/DOCX)
        from src.utils.document_parser import DocumentParser

        doc_parser = DocumentParser()
        parsed_data = doc_parser.parse_document(Path(args.document))
        patient_data = parsed_data.get("patient")
        blood_tests_data = parsed_data.get("blood_tests")
    elif args.json:
        if args.patient or args.blood_tests:
            print("Błąd: Nie można używać --json razem z --patient lub --blood-tests")
            sys.exit(1)

        json_parser = JSONParser()
        parsed_data = json_parser.parse_document(Path(args.json))
        patient_data = parsed_data.get("patient")
        blood_tests_data = parsed_data.get("blood_tests")
    else:
        if not args.patient or not args.blood_tests:
            print(
                "Błąd: Należy podać --json, --document lub oba pliki: --patient i --blood-tests"
            )
            print("Użycie:")
            print("  Opcja 1: --json <ścieżka_do_pliku.json>")
            print("  Opcja 2: --document <ścieżka_do_dokumentu.pdf lub .docx>")
            print(
                "  Opcja 3: --patient <ścieżka_do_pliku_pacjenta.json> --blood-tests <ścieżka_do_pliku_badan.json>"
            )
            sys.exit(1)

        json_parser = JSONParser()
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

    loader = DataLoader(DATA_DIR)

    validator = Validator()

    patient = validator.validate_patient(patient_data)
    blood_tests = validator.validate_blood_tests(blood_tests_data)

    if args.web:
        run_web(
            patient,
            blood_tests,
            host=args.host,
            port=args.port,
            no_browser=args.no_browser,
        )
        return True

    print("Medical Supplement Advisor")
    print("=" * 40)

    reference_ranges = loader.load_reference_ranges()
    supplements = loader.load_supplements()
    timing_rules = loader.load_timing_rules()
    dosage_rules = loader.load_dosage_rules()

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

    return True


def run_gui():
    """Run GUI interface (PyQt5)."""
    from PyQt5.QtWidgets import QApplication
    from src.gui.main_window import MainWindow

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


def main():
    """Main entry point - decides whether to run CLI or GUI based on arguments."""
    # Check if we're running with arguments
    if len(sys.argv) > 1:
        # Has arguments - try CLI first
        if run_cli():
            return  # CLI ran successfully
        # If CLI returned False, no valid CLI args were provided

    # No CLI arguments or CLI returned False - run GUI
    run_gui()


if __name__ == "__main__":
    main()
