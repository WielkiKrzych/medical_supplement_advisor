# 🧪 Medical Supplement Advisor

> Intelligent supplement recommendations based on your blood test results

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![CI/CD](https://github.com/WielkiKrzych/medical_supplement_advisor/workflows/CI/badge.svg)](https://github.com/WielkiKrzych/medical_supplement_advisor/actions)
[![Code Quality: Pylint](https://img.shields.io/badge/code%20quality-pylint%20%3E%3D9.0-brightgreen)](https://www.pylint.org/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Coverage](https://img.shields.io/badge/coverage-comprehensive-brightgreen)](https://github.com/WielkiKrzych/medical_supplement_advisor)
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
- **Automated Blood Test Analysis**: Compare your results against medical reference ranges
- **Rule-Based Recommendations**: Advanced engine matches supplements to specific deficiencies
- **Priority-Based Suggestions**: Supplements ordered by importance for your health

### 📊 Comprehensive Data Management
- **Multiple Input Formats**: Support for JSON, DOCX, and manual entry
- **Flexible Patient Profiles**: Age, conditions, and health considerations
- **Rich Reference Data**: Extensive supplement database with dosages and timing rules

### 🎨 User-Friendly Interface
- **Modern GUI**: Built with PyQt5 for a smooth desktop experience
- **CLI Alternative**: Command-line interface for power users and automation
- **PDF Reports**: Generate professional, printable supplement reports

### 🛡️ Quality & Reliability
- **Type-Safe Code**: 100% type annotated with Pydantic models
- **Comprehensive Testing**: Extensive test coverage for core business logic
- **CI/CD Pipeline**: Automated testing on every push and pull request
- **Code Quality**: Enforced with Pylint, Black, and Isort

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
python src/main.py --input examples/sample_blood_tests.json --output recommendations.pdf
```

**Command Options**:
- `--input`: Path to input file (JSON or DOCX)
- `--output`: Path for output PDF report
- `--format`: Input format (`json` or `docx`)

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
│   ├── supplements.json        # Supplement database
│   ├── timing_rules.json      # When to take supplements
│   └── dosage_rules.json      # Dosage recommendations
├── 📂 src/
│   ├── 📂 models/            # Pydantic data models
│   ├── 📂 core/              # Business logic
│   │   ├── analyzer.py       # Blood test analysis
│   │   ├── rule_engine.py    # Rule matching
│   │   └── recommendation_engine.py  # Recommendations
│   ├── 📂 utils/            # Helper utilities
│   │   ├── exceptions.py     # Custom exceptions
│   │   ├── validator.py      # Data validation
│   │   ├── data_loader.py    # JSON loading
│   │   ├── formatter.py     # PDF generation
│   │   └── json_parser.py   # JSON parsing
│   ├── 📂 gui/              # PyQt5 GUI
│   │   ├── app.py           # Application entry
│   │   └── main_window.py   # Main window
│   └── main.py              # CLI entry point
├── 📂 tests/                # Unit tests
├── 📂 examples/              # Sample data
├── 📂 .github/workflows/     # CI/CD pipelines
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
| **RuleEngine** | Pattern matching for supplements | ✓ |
| **RecommendationEngine** | Recommendation generation | ✓ |
| **Models** | Pydantic data model validation | ✓ |

Coverage reports are automatically uploaded to CI.

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

✨ **Custom Exception Classes**
- `ValidationError`: Data structure validation
- `DataLoaderError`: JSON file loading
- `RuleEngineError`: Rule engine errors
- `AnalysisError`: Blood test analysis

✨ **Enhanced Validation**
- Exception-based error handling
- Clear error messages with context
- Proper error propagation

✨ **Code Quality**
- Eliminated code duplication
- Single source of truth for priority ordering
- Full type safety with `str | None` unions

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
