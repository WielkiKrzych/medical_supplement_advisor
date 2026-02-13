# 🧪 Medical Supplement Advisor

> Intelligent supplement recommendations based on your blood test results

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![CI/CD](https://github.com/WielkiKrzych/medical_supplement_advisor/workflows/CI/badge.svg)](https://github.com/WielkiKrzych/medical_supplement_advisor/actions)
[![Code Quality: Pylint](https://img.shields.io/badge/code%20quality-pylint%20%3E%3D7.5-brightgreen)](https://www.pylint.org/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-39%20passed-brightgreen)](https://github.com/WielkiKrzych/medical_supplement_advisor)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Transform your blood test results into personalized supplement recommendations with a modern, intuitive interface.

---

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [✨ Features](#-features)
- [📸 Screenshots](#-screenshots)
- [📦 Installation](#-installation)
- [🎯 Usage](#-usage)
- [🏗️ Project Structure](#️-project-structure)
- [🧪 Testing](#-testing)
- [🛠️ Development](#️-development)
- [🗺️ Roadmap & Future Plans](#️-roadmap--future-plans)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🚀 Quick Start

Get up and running in under 5 minutes:

```bash
# 1. Clone the repository
git clone https://github.com/WielkiKrzych/medical_supplement_advisor.git
cd medical_supplement-advisor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python src/main.py
```

That's it! 🎉 The GUI will launch and you can start analyzing your blood tests.

**Expected Output**:
- Interactive GUI with patient data input
- Blood test result upload/parsing
- Personalized supplement recommendations
- PDF report generation

---

## ✨ Features

### 🔬 Intelligent Analysis
- **Advanced Clinical Algorithm**: Based on 60+ blood test parameters with detailed interpretations
- **Pattern Recognition**: Identifies complex patterns (anemia, PCOS, insulin resistance, thyroid issues)
- **Detailed Interpretations**: Each abnormal result includes possible causes and clinical context
- **Rule-Based Recommendations**: Advanced engine matches supplements to specific deficiencies
- **Priority-Based Suggestions**: Supplements ordered by importance for your health
- **Curve Analysis**: Support for glucose and insulin curve interpretation
- **Ratio Analysis**: Automatic calculation of important ratios (HDL:LDL, AST:ALT, LH:FSH, etc.)

### 📊 Comprehensive Data Management
- **Multiple Input Formats**: Support for JSON, DOCX, PDF, and manual entry
- **Flexible Patient Profiles**: Age, conditions, and health considerations
- **Rich Reference Data**: 60+ blood test parameters with clinical interpretations
- **Commercial Supplement Database**: 70+ supplements with dosages and indications
- **Clinical Rules Engine**: Pattern matching for complex health conditions

### 🎨 User-Friendly Interface
- **Modern GUI**: Built with PyQt5 for a smooth desktop experience
- **CLI Alternative**: Command-line interface for power users and automation
- **PDF Reports**: Generate professional, printable supplement reports

### 🛡️ Quality & Reliability
- **Type-Safe Code**: 100% type annotated with Pydantic models
- **Comprehensive Testing**: 39 tests covering core business logic and new algorithm
- **CI/CD Pipeline**: Automated testing on every push and pull request
- **Code Quality**: Enforced with Pylint, Black, and Isort
- **Security**: Path traversal protection, filename sanitization, file size limits
- **Clinical Accuracy**: Based on real clinical data and protocols
- **Internationalization**: i18n support with language persistence

### 🚀 Developer Experience
- **Clean Architecture**: Well-organized, modular codebase
- **Extensible Design**: Easy to add new rules, supplements, or input formats
- **Documentation**: Inline docstrings and type hints throughout
- **Build System**: PyInstaller configuration for standalone executables

---

## 📸 Screenshots

> *Note: Screenshots will be added as the project evolves. For now, here's what you can expect:*

### Main Application Window
- Patient information entry
- Blood test data input
- Real-time validation

### Recommendation Results
- Supplement suggestions with priorities
- Dosage and timing information
- One-click PDF export

### PDF Report Preview
- Professional medical report
- Supplement schedule
- Visual deficiency indicators

---

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Standard Installation

```bash
git clone https://github.com/WielkiKrzych/medical_supplement_advisor.git
cd medical-supplement-advisor
pip install -r requirements.txt
```

### Development Installation

For contributors who want to work on the codebase:

```bash
# Install development dependencies
pip install -r requirements.txt
pip install -e .

# Verify installation
pytest --version
black --version
```

### Building Standalone Executable

Create a portable executable:

```bash
python build_app.py
```

The executable will be generated in the `dist/` directory.

---

## 🎯 Usage

### GUI Application

Launch the graphical interface:

```bash
python src/main.py
```

**Workflow**:
1. Enter patient information (name, age, medical conditions)
2. Input blood test results (test name, value, unit)
3. Click "Analyze" to process results
4. Review supplement recommendations
5. Export PDF report (optional)

### CLI Application

Use the command-line interface:

```bash
# Single JSON file with patient and blood tests
python src/main.py --json examples/sample_blood_tests.json

# Separate patient and blood test files
python src/main.py --patient examples/sample_patient.json --blood-tests examples/sample_blood_tests.json

# Parse PDF or DOCX document
python src/main.py --document lab_results.pdf
```

**Command Options**:
- `--json`: Path to combined JSON file (patient + blood tests)
- `--patient`: Path to patient JSON file (requires --blood-tests)
- `--blood-tests`: Path to blood tests JSON file (requires --patient)
- `--document`: Path to PDF or DOCX file for automatic parsing

**Note**: Options `--json`, `--document`, and `--patient`/`--blood-tests` are mutually exclusive.

### Input Format

**JSON Example**:
```json
{
  "patient": {
    "name": "John",
    "surname": "Doe",
    "age": 45,
    "medical_conditions": ["vitamin_d_deficiency"]
  },
  "blood_tests": [
    {
      "name": "Vitamin D",
      "value": 15,
      "unit": "ng/mL"
    }
  ]
}
```

**Supported Blood Tests** (60+ parameters):

**Morfologia**:
- WBC, RDW, PDW, Neutrofile, Bazofile, Limfocyty, Monocyty, Eozynofile
- Hemoglobina, Erytrocyty, Hematokryt, MCV, MCH, MCHC

**Vitamins**:
- Witamina D3, B12, B9, C, A, E, K2

**Minerals & Metabolism**:
- Żelazo, Ferrytyna, Transferryna, Cynk, Selen, Magnez, Potas, Sód
- Fosfor, Fosfataza Alkaliczna, Ceruloplazmina, Jod w moczu

**Thyroid Panel**:
- TSH, FT3, FT4, Anty-TG, Anty-TPO, TRAb

**Lipid Profile**:
- Cholesterol, HDL, LDL, Trójglicerydy (TG)
- Ratios: HDL:LDL, HDL:TG

**Liver Function**:
- AST, ALT, GGTP, Stosunek AST:ALT

**Glucose & Insulin**:
- Glukoza (krzywa), Insulina (krzywa), HbA1c, HOMA-IR

**Hormones**:
- Testosteron, DHT, DHEAS, Androstendion, SHBG
- Progesteron, Estradiol, LH, FSH, Prolaktyna, Kortyzol
- Ratios: LH:FSH, Estradiol:Progesteron

**Inflammatory Markers**:
- CRP, OB (Odczyn Biernackiego)

**Enzymes**:
- DAO (diaminooksydaza), Peroksydaza Glutationowa (GPx)

**Supported File Formats**:
- JSON files (structured data)
- PDF files (lab reports with OCR support)
- DOCX files (Word documents)
- Maximum file size: 50MB

### Output Format

The application generates a professional PDF report containing:
- Patient information
- Blood test analysis
- Supplement recommendations (name, dosage, timing, priority)
- Health notes and recommendations

---

## 🏗️ Project Structure

```
medical-supplement-advisor/
├── 📂 data/                    # Reference data
│   ├── reference_ranges.json   # Blood test reference ranges
│   ├── reference_ranges_v2.json # Advanced clinical ranges (60+ tests)
│   ├── supplements.json        # Supplement database (21 supplements)
│   ├── supplements_v2.json     # Commercial supplements (70+ products)
│   ├── interpretation_rules.json # Clinical interpretation rules
│   ├── clinical_thresholds.json # Configurable clinical thresholds
│   ├── test_categories.json    # Test category definitions
│   ├── timing_rules.json      # When to take supplements
│   └── dosage_rules.json      # Dosage recommendations
├── 📂 i18n/                   # Internationalization
│   └── pl.json               # Polish translations
├── 📂 config/                 # Configuration
│   └── user_settings.json     # User preferences (language, etc.)
├── 📂 src/
│   ├── 📂 models/            # Pydantic data models
│   │   ├── blood_test.py     # Blood test model
│   │   ├── patient.py        # Patient model
│   │   ├── recommendation.py # Recommendation model
│   │   ├── supplement.py     # Supplement model
│   │   └── test_analysis.py  # Advanced analysis models
│   ├── 📂 core/              # Business logic
│   │   ├── analyzer.py       # Blood test analysis
│   │   ├── advanced_analyzer.py  # Advanced clinical analysis
│   │   ├── interpretation_engine.py # Detailed test interpretation
│   │   ├── rule_engine.py    # Rule matching
│   │   └── recommendation_engine.py  # Recommendations
│   ├── 📂 utils/            # Helper utilities
│   │   ├── exceptions.py     # Custom exceptions
│   │   ├── validator.py      # Data validation
│   │   ├── data_loader.py    # JSON loading with caching
│   │   ├── formatter.py     # PDF generation
│   │   ├── json_parser.py   # JSON parsing
│   │   ├── document_parser.py # PDF/DOCX parsing with OCR
│   │   ├── i18n.py          # Internationalization utilities
│   │   └── logger.py        # Application logging
│   ├── 📂 gui/              # PyQt5 GUI
│   │   ├── app.py           # Application entry
│   │   └── main_window.py   # Main window with security features
│   └── main.py              # CLI entry point
├── 📂 tests/                # Unit tests (39 tests)
├── 📂 examples/              # Sample data
├── 📂 .github/workflows/     # CI/CD pipelines
├── 📂 logs/                  # Application logs
├── 📄 config.py            # Configuration
├── 📄 pyproject.toml       # Project metadata & tool config
├── 📄 requirements.txt      # Dependencies
└── 📄 README.md            # This file
```

---

## 🧪 Testing

### Run All Tests

```bash
# Full test suite with coverage
pytest --cov=src --cov-report=html:htmlcov --cov-report=term-missing tests/

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Run Specific Tests

```bash
# Analyzer tests
pytest tests/test_analyzer.py -v

# Rule engine tests
pytest tests/test_rule_engine.py -v

# Recommendation engine tests
pytest tests/test_recommendation_engine.py -v
```

### Test Coverage

The project maintains comprehensive test coverage:

| Module | Description | Tests |
|--------|-------------|-------|
| **Analyzer** | Blood test status determination | ✓ |
| **AdvancedAnalyzer** | Clinical pattern recognition | ✓ |
| **InterpretationEngine** | Detailed test interpretation | ✓ |
| **RuleEngine** | Pattern matching for supplements | ✓ |
| **RecommendationEngine** | Recommendation generation | ✓ |
| **Models** | Pydantic data model validation | ✓ |
| **Security** | Path validation, sanitization | ✓ |
| **Logging** | Application logging system | ✓ |

Coverage reports are automatically uploaded to CI.

### Security Features

The application includes multiple security layers:

- **Path Traversal Protection**: All file paths are validated before access
- **Filename Sanitization**: Special characters are removed from filenames
- **File Size Limits**: Maximum file size (50MB) prevents DoS attacks
- **Input Validation**: All user inputs are validated using Pydantic models
- **Safe PDF Opening**: PDF files are verified before opening with system applications

---

## 🛠️ Development

### Code Quality Tools

The project uses modern Python development tools:

| Tool | Purpose | Configuration |
|------|---------|---------------|
| **Black** | Code formatter | `pyproject.toml` (100 char line length) |
| **Isort** | Import organizer | `pyproject.toml` (Black-compatible) |
| **Pylint** | Static analysis | `.pylintrc` (Score ≥ 9.0) |
| **Pytest** | Testing framework | `pyproject.toml` |
| **MyPy** | Type checking | Configured in `pyproject.toml` |

### Development Workflow

```bash
# 1. Make changes to code
# 2. Run tests locally
pytest

# 3. Check code quality
pylint src/
black --check src/
isort --check-only src/

# 4. Commit changes
git add .
git commit -m "feat: add new feature"

# 5. Push to trigger CI/CD
git push
```

### Recent Improvements

✨ **Advanced Clinical Algorithm (v2.0)**
- 60+ blood test parameters with detailed interpretations
- Pattern recognition for complex conditions (anemia, PCOS, insulin resistance, thyroid)
- Curve analysis for glucose and insulin
- Ratio analysis (HDL:LDL, AST:ALT, LH:FSH, etc.)
- 70+ commercial supplements with dosages and indications
- Clinical interpretation rules based on real medical data

✨ **Security Enhancements**
- Path traversal protection in file operations
- Filename sanitization to prevent injection attacks
- File size limits (50MB) to prevent DoS attacks
- Secure PDF opening with path validation

✨ **Custom Exception Classes**
- `ValidationError`: Data structure validation
- `DataLoaderError`: JSON file loading with detailed context
- `RuleEngineError`: Rule engine errors
- `AnalysisError`: Blood test analysis

✨ **Enhanced Validation & Error Handling**
- Exception-based error handling throughout the codebase
- Clear error messages with context
- Proper error propagation
- Comprehensive JSON parsing error handling

✨ **Performance Optimizations**
- Data caching with `@lru_cache` for reference data
- Reduced file I/O operations
- Optimized data loading

✨ **Code Quality**
- Eliminated code duplication
- Single source of truth for priority ordering
- Full type safety with `str | None` unions
- Added logging system for better debugging
- 39 comprehensive tests (100% passing)

✨ **Internationalization (i18n) v2.1**
- Full i18n support with translation files (`i18n/pl.json`)
- Language persistence across application restarts
- All hardcoded strings moved to translation files
- Patterns and ratio interpretations now translatable
- Easy to add new languages by creating new JSON files

✨ **Configurable Clinical Thresholds**
- Clinical thresholds loaded from `clinical_thresholds.json`
- Fallback thresholds when configuration fails
- Support for functional and lab reference ranges
- Easy to customize for different clinical protocols

✨ **Bug Fixes & Improvements**
- PDF filename collision prevention with timestamps
- Translation key validation and fallbacks
- Priority parameter validation in PDF generation
- Logger imports optimized to module level
- Improved error handling with proper logging

---

## 🗺️ Roadmap & Future Plans

### Version 2.2 (In Progress)
- [ ] **Web Interface**: Flask/FastAPI web application for browser access
- [ ] **Multi-language Support**: English translations alongside Polish
- [ ] **Enhanced PDF Reports**: Charts, graphs, and visual deficiency indicators

### Version 2.3 (Planned)
- [ ] **Machine Learning**: Personalized recommendations based on historical data
- [ ] **Drug Interactions**: Alert system for supplement-medication interactions
- [ ] **Mobile Companion**: iOS/Android app for tracking and reminders

### Version 3.0 (Long-term Vision)
- [ ] **Healthcare Provider Integration**: HL7 FHIR compatibility
- [ ] **Telemedicine API**: Integration with telehealth platforms
- [ ] **Community Features**: Anonymous data sharing for research
- [ ] **AI Chatbot**: Natural language interface for health queries

### Contributing to Roadmap

Have ideas? We'd love to hear them!
- 🐛 [Report bugs](https://github.com/WielkiKrzych/medical_supplement_advisor/issues)
- 💡 [Request features](https://github.com/WielkiKrzych/medical_supplement_advisor/issues)
- 🗣️ [Join discussions](https://github.com/WielkiKrzych/medical_supplement_advisor/discussions)

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed
4. **Run tests and quality checks**
   ```bash
   pytest
   pylint src/
   black --check src/
   isort --check-only src/
   ```
5. **Commit your changes**
   ```bash
   git commit -m "feat: add your feature description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

### Contribution Guidelines

- **Code Style**: Follow PEP 8, enforced by Black and Isort
- **Type Hints**: Add type annotations to all new code
- **Documentation**: Update docstrings for public APIs
- **Tests**: Maintain test coverage above 80%
- **Commits**: Use conventional commit messages (`feat:`, `fix:`, `docs:`, etc.)

### Getting Help

- Open an issue for bugs or feature requests
- Join discussions for questions and ideas
- Check existing issues before creating new ones

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- [GitHub Repository](https://github.com/WielkiKrzych/medical_supplement_advisor)
- [Issues](https://github.com/WielkiKrzych/medical_supplement_advisor/issues)
- [Pull Requests](https://github.com/WielkiKrzych/medical_supplement_advisor/pulls)
- [Actions](https://github.com/WielkiKrzych/medical_supplement_advisor/actions)

---

<div align="center">

**Made with ❤️ for better health through intelligent supplement recommendations**

[⬆ Back to Top](#-medical-supplement-advisor)

</div>
