import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QGroupBox,
    QApplication,
    QProgressBar,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.utils.json_parser import JSONParser
from src.utils.validator import Validator
from src.core.recommendation_engine import RecommendationEngine
from src.utils.formatter import PDFFormatter
from src.utils.data_loader import DataLoader
from src.utils.document_parser import DocumentParser
from config import DATA_DIR, OUTPUT_DIR


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medical Supplement Advisor")
        self.setMinimumSize(700, 500)
        self.json_parser = JSONParser()
        self.document_parser = DocumentParser()
        self.selected_json_file = None
        self.selected_document_file = None
        self.output_pdf_path = None

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("Medical Supplement Advisor")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        description_label = QLabel(
            "Wybierz plik z wynikami badań (JSON, PDF lub DOCX) "
            "aby wygenerować rekomendację suplementacji.\n"
            "Dokumenty PDF i DOCX zostaną automatycznie przetworzone."
        )
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(description_label)
        layout.addSpacing(10)

        input_group = QGroupBox("Dane wejściowe")
        input_layout = QVBoxLayout()

        file_selector_layout = QHBoxLayout()
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("Wybierz plik (JSON, PDF lub DOCX)...")
        self.file_path_edit.setReadOnly(True)
        file_selector_layout.addWidget(self.file_path_edit)

        self.browse_button = QPushButton("Przeglądaj...")
        self.browse_button.clicked.connect(self.browse_json_file)
        file_selector_layout.addWidget(self.browse_button)

        input_layout.addLayout(file_selector_layout)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        self.generate_button = QPushButton("Generuj raport PDF")
        self.generate_button.setEnabled(False)
        self.generate_button.setMinimumHeight(40)
        self.generate_button.clicked.connect(self.generate_pdf)
        layout.addWidget(self.generate_button)

        layout.addSpacing(10)

        output_group = QGroupBox("Status")
        output_layout = QVBoxLayout()

        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(100)
        output_layout.addWidget(self.status_text)

        self.output_label = QLabel("Plik PDF: Nie wygenerowano")
        self.output_label.setStyleSheet("color: gray;")
        output_layout.addWidget(self.output_label)

        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        self.open_pdf_button = QPushButton("Otwórz PDF")
        self.open_pdf_button.setEnabled(False)
        self.open_pdf_button.clicked.connect(self.open_pdf)
        layout.addWidget(self.open_pdf_button)

        layout.addStretch()

    def browse_json_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz plik z wynikami badań",
            "",
            "Wszystkie obsługiwane formaty (*.json *.pdf *.docx);;Pliki JSON (*.json);;Dokumenty PDF (*.pdf);;Dokumenty Word (*.docx);;Wszystkie pliki (*)",
        )
        if file_path:
            file_path_obj = Path(file_path)
            file_ext = file_path_obj.suffix.lower()

            if file_ext == ".json":
                self.selected_json_file = file_path_obj
                self.selected_document_file = None
            elif file_ext in [".pdf", ".docx"]:
                self.selected_document_file = file_path_obj
                self.selected_json_file = None
            else:
                self.status_text.clear()
                self.status_text.append(f"Nieobsługiwany format pliku: {file_ext}")
                return

            self.file_path_edit.setText(file_path)
            self.generate_button.setEnabled(True)
            self.status_text.clear()
            self.status_text.append(f"Wybrano plik: {file_path_obj.name}")

            # Show file type info
            if file_ext in [".pdf", ".docx"]:
                self.status_text.append(
                    "Format: Dokument - zostanie automatycznie przekonwertowany"
                )
            else:
                self.status_text.append("Format: JSON")

    def generate_pdf(self):
        if not self.selected_json_file and not self.selected_document_file:
            return

        self.generate_button.setEnabled(False)
        self.status_text.append("Ładowanie danych...")

        try:
            # Parse based on file type
            if self.selected_document_file:
                self.status_text.append("Przetwarzanie dokumentu (PDF/DOCX)...")
                parsed_data = self.document_parser.parse_document(
                    self.selected_document_file
                )
            else:
                self.status_text.append("Przetwarzanie pliku JSON...")
                parsed_data = self.json_parser.parse_document(self.selected_json_file)

            patient_data = parsed_data.get("patient")
            blood_tests_data = parsed_data.get("blood_tests")

            if not patient_data or not patient_data.get("name"):
                raise ValueError("Nie znaleziono danych pacjenta")

            if not blood_tests_data:
                raise ValueError("Nie znaleziono badań krwi")

            self.status_text.append("Walidacja danych...")
            validator = Validator()
            patient = validator.validate_patient(patient_data)
            blood_tests = validator.validate_blood_tests(blood_tests_data)

            self.status_text.append("Ładowanie danych referencyjnych...")
            loader = DataLoader(DATA_DIR)
            reference_ranges = loader.load_reference_ranges()
            supplements = loader.load_supplements()
            timing_rules = loader.load_timing_rules()
            dosage_rules = loader.load_dosage_rules()

            self.status_text.append("Generowanie rekomendacji...")
            recommendation_engine = RecommendationEngine(
                reference_ranges=reference_ranges,
                supplements=supplements,
                timing_rules=timing_rules,
                dosage_rules=dosage_rules,
            )
            recommendation = recommendation_engine.generate_recommendation(
                patient, blood_tests
            )

            self.status_text.append("Generowanie PDF...")
            formatter = PDFFormatter(OUTPUT_DIR)
            self.output_pdf_path = formatter.generate_pdf(recommendation)

            self.status_text.append(f"✓ Utworzono: {self.output_pdf_path.name}")
            self.status_text.append(
                f"✓ Liczba suplementów: {len(recommendation.supplements)}"
            )

            self.output_label.setText(f"Plik PDF: {self.output_pdf_path}")
            self.output_label.setStyleSheet("color: green;")
            self.open_pdf_button.setEnabled(True)

        except FileNotFoundError as e:
            QMessageBox.critical(self, "Błąd", f"Plik nie istnieje: {e}")
            self.status_text.append(f"✗ Błąd: {e}")
        except ValueError as e:
            QMessageBox.critical(self, "Błąd danych", f"Błąd w danych: {e}")
            self.status_text.append(f"✗ Błąd: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił nieoczekiwany błąd: {e}")
            self.status_text.append(f"✗ Błąd: {e}")
        finally:
            self.generate_button.setEnabled(True)

    def open_pdf(self):
        """Open the generated PDF file with the default system application."""
        if not self.output_pdf_path or not self.output_pdf_path.exists():
            QMessageBox.warning(self, "Ostrzeżenie", "Plik PDF nie istnieje.")
            return

        # Validate that the path is within the expected output directory
        try:
            from config import OUTPUT_DIR

            resolved_path = self.output_pdf_path.resolve()
            resolved_output_dir = OUTPUT_DIR.resolve()
            if not str(resolved_path).startswith(str(resolved_output_dir)):
                QMessageBox.critical(
                    self,
                    "Błąd bezpieczeństwa",
                    "Ścieżka pliku jest poza dozwolonym katalogiem.",
                )
                return
        except Exception:
            # If validation fails, don't proceed
            QMessageBox.critical(self, "Błąd", "Nie można zweryfikować ścieżki pliku.")
            return

        import subprocess
        import platform

        try:
            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.run(["open", str(self.output_pdf_path)], check=True)
            elif system == "Windows":
                subprocess.run(
                    ["start", "", str(self.output_pdf_path)], shell=True, check=True
                )
            else:  # Linux and other Unix-like
                subprocess.run(["xdg-open", str(self.output_pdf_path)], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Błąd", f"Nie można otworzyć pliku PDF: {e}")
        except Exception as e:
            QMessageBox.critical(
                self, "Błąd", f"Wystąpił błąd podczas otwierania pliku: {e}"
            )
