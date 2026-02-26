<div align="center">

# 🧪 Medical Supplement Advisor

### *Transform Your Blood Tests Into Personalized Health Insights*

<img src="https://img.shields.io/badge/python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"/>
<img src="https://img.shields.io/badge/code%20style-black-000000?style=for-the-badge" alt="Code Style: Black"/>
<img src="https://img.shields.io/badge/tests-39%20passed-brightgreen?style=for-the-badge" alt="Tests"/>
<img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge" alt="License"/>
<img src="https://img.shields.io/badge/coverage-80%25+-green?style=for-the-badge" alt="Coverage"/>

[![CI/CD](https://github.com/WielkiKrzych/medical_supplement_advisor/workflows/CI/badge.svg)](https://github.com/WielkiKrzych/medical_supplement_advisor/actions)
[![Code Quality: Pylint](https://img.shields.io/badge/pylint-%3E%3D7.5-brightgreen)](https://www.pylint.org/)

**🩸 60+ Blood Parameters • 📊 70+ Supplements • 🎯 Clinical Algorithm • 🌍 i18n Ready**

</div>

---

## 📑 Navigation

| 🚀 Getting Started | 📖 Documentation | 🛠️ For Developers |
|:-----------------:|:----------------:|:-----------------:|
| [Quick Start](#-quick-start) | [Features](#-features) | [Installation](#-installation) |
| [Usage](#-usage) | [Input Formats](#-input-format) | [Testing](#-testing) |
| [Examples](#-examples) | [Output](#-output-format) | [Contributing](#-contributing) |

---

## 🚀 Quick Start

> ⏱️ **Get up and running in under 5 minutes!**

```bash
# 1️⃣ Clone the repository
git clone https://github.com/WielkiKrzych/medical_supplement_advisor.git
cd medical_supplement_advisor

# 2️⃣ Install dependencies
pip install -r requirements.txt

# 3️⃣ Launch the application
python src/main.py
```

<div align="center">

| 🖥️ GUI Mode | 💻 CLI Mode |
|:-----------:|:-----------:|
| `python src/main.py` | `python src/main.py --json data.json` |
| Interactive interface | Automation & scripting |

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔬 Intelligent Analysis

- 🧬 **60+ Blood Parameters** — Comprehensive clinical analysis
- 🎯 **Pattern Recognition** — Anemia, PCOS, insulin resistance, thyroid
- 📈 **Curve Analysis** — Glucose & insulin curves
- 📐 **Ratio Calculation** — HDL:LDL, AST:ALT, LH:FSH
- 🏥 **Clinical Accuracy** — Real medical protocols

</td>
<td width="50%">

### 📊 Data Management

- 📄 **Multi-Format Input** — JSON, PDF, DOCX, manual
- 💾 **70+ Supplements** — Commercial product database
- 👤 **Patient Profiles** — Age, conditions, preferences
- ⚙️ **Configurable Rules** — Custom clinical thresholds
- 🌍 **i18n Support** — Polish translations included

</td>
</tr>
<tr>
<td width="50%">

### 🎨 User Experience

- 🖼️ **Modern GUI** — PyQt5 desktop experience
- ⌨️ **CLI Alternative** — Power user interface
- 📑 **PDF Reports** — Professional medical documents
- 🔔 **Real-time Validation** — Instant feedback
- 📱 **Responsive Design** — Clean, intuitive layout

</td>
<td width="50%">

### 🛡️ Quality & Security

- ✅ **39 Tests** — 100% passing, comprehensive coverage
- 🔒 **Security First** — Path traversal protection, sanitization
- 📝 **Type Safety** — 100% annotated with Pydantic
- 🔄 **CI/CD Pipeline** — Automated testing on every push
- 📊 **Code Quality** — Pylint, Black, Isort enforced

</td>
</tr>
</table>

---

## 📸 Application Preview

> 🎬 *Screenshots coming soon! Here's what to expect:*

<div align="center">

| 🖥️ Main Window | 📊 Analysis Results | 📄 PDF Report |
|:--------------:|:------------------:|:-------------:|
| Patient data input | Supplement recommendations | Professional document |
| Blood test entry | Priority-ranked suggestions | Visual deficiency indicators |
| Real-time validation | Dosage & timing info | Exportable & printable |

</div>

---

## 📦 Installation

### 📋 Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| 🐍 Python | 3.11+ | Required |
| 📦 pip | Latest | Package manager |
| 🖥️ OS | macOS/Linux/Windows | Cross-platform |

### 🔧 Installation Options

<details>
<summary><b>📦 Standard Installation</b></summary>

```bash
git clone https://github.com/WielkiKrzych/medical_supplement_advisor.git
cd medical_supplement_advisor
pip install -r requirements.txt
```
</details>

<details>
<summary><b>👨‍💻 Development Installation</b></summary>

```bash
# Install with development dependencies
pip install -r requirements.txt
pip install -e .

# Verify installation
pytest --version && black --version && pylint --version
```
</details>

<details>
<summary><b>📦 Build Standalone Executable</b></summary>

```bash
python build_app.py
# Executable generated in dist/ directory
```
</details>

---

## 🎯 Usage

### 🖥️ GUI Application

```bash
python src/main.py
```

**Workflow:**

```
📝 Enter Patient Info → 🩸 Input Blood Tests → 🔬 Analyze → 💊 Get Recommendations → 📄 Export PDF
```

### 💻 CLI Application

```bash
# 📄 Single JSON file
python src/main.py --json examples/sample_blood_tests.json

# 👤 Separate patient & test files
python src/main.py --patient patient.json --blood-tests tests.json

# 📑 Parse PDF/DOCX document
python src/main.py --document lab_results.pdf
```

**CLI Options:**

| Option | Description | Required |
|--------|-------------|----------|
| `--json` | Combined JSON file (patient + tests) | One of the below |
| `--patient` + `--blood-tests` | Separate files | |
| `--document` | PDF/DOCX for parsing | |

---

## 📝 Input Format

### JSON Example

```json
{
  "patient": {
    "name": "John",
    "surname": "Doe", 
    "age": 45,
    "medical_conditions": ["vitamin_d_deficiency"]
  },
  "blood_tests": [
    {"name": "Vitamin D", "value": 15, "unit": "ng/mL"},
    {"name": "Ferritin", "value": 25, "unit": "ng/mL"}
  ]
}
```

### 🩸 Supported Blood Tests (60+ Parameters)

<table>
<tr>
<th>🫀 Category</th>
<th>🔬 Tests</th>
</tr>
<tr>
<td><b>📊 Morfologia</b></td>
<td>WBC • RDW • PDW • Neutrofile • Bazofile • Limfocyty • Monocyty • Eozynofile • Hemoglobina • Erytrocyty • Hematokryt • MCV • MCH • MCHC</td>
</tr>
<tr>
<td><b>💊 Vitamins</b></td>
<td>D3 • B12 • B9 • C • A • E • K2</td>
</tr>
<tr>
<td><b>⚗️ Minerals</b></td>
<td>Żelazo • Ferrytyna • Transferryna • Cynk • Selen • Magnez • Potas • Sód • Fosfor • Fosfataza Alkaliczna • Ceruloplazmina • Jod</td>
</tr>
<tr>
<td><b>🦋 Thyroid</b></td>
<td>TSH • FT3 • FT4 • Anty-TG • Anty-TPO • TRAb</td>
</tr>
<tr>
<td><b>❤️ Lipids</b></td>
<td>Cholesterol • HDL • LDL • Trójglicerydy • HDL:LDL Ratio • HDL:TG Ratio</td>
</tr>
<tr>
<td><b>🫀 Liver</b></td>
<td>AST • ALT • GGTP • AST:ALT Ratio</td>
</tr>
<tr>
<td><b>🍬 Glucose</b></td>
<td>Glukoza (krzywa) • Insulina (krzywa) • HbA1c • HOMA-IR</td>
</tr>
<tr>
<td><b>🧬 Hormones</b></td>
<td>Testosteron • DHT • DHEAS • Androstendion • SHBG • Progesteron • Estradiol • LH • FSH • Prolaktyna • Kortyzol</td>
</tr>
<tr>
<td><b>🔥 Inflammation</b></td>
<td>CRP • OB (Odczyn Biernackiego)</td>
</tr>
<tr>
<td><b>⚗️ Enzymes</b></td>
<td>DAO (diaminooksydaza) • Peroksydaza Glutationowa (GPx)</td>
</tr>
</table>

### 📁 Supported File Formats

| Format | Max Size | Notes |
|--------|----------|-------|
| 📄 JSON | 50MB | Structured data |
| 📕 PDF | 50MB | OCR support |
| 📘 DOCX | 50MB | Word documents |

---

## 📤 Output Format

The application generates a **professional PDF report** containing:

<div align="center">

| 👤 Patient Info | 🩸 Blood Analysis | 💊 Recommendations | 📝 Health Notes |
|:---------------:|:-----------------:|:------------------:|:---------------:|
| Name, age, conditions | Test results & status | Supplements & dosage | Lifestyle tips |
| Medical history | Reference ranges | Priority ranking | Warnings & alerts |
| | Interpretations | Timing instructions | Follow-up suggestions |

</div>

---

## 🏗️ Project Structure

```
medical-supplement-advisor/
├── 📂 data/                      # Reference data & rules
│   ├── 📄 reference_ranges.json  # Blood test ranges
│   ├── 📄 supplements_v2.json    # 70+ commercial supplements
│   ├── 📄 interpretation_rules.json
│   └── 📄 clinical_thresholds.json
│
├── 📂 src/
│   ├── 📂 models/               # Pydantic data models
│   │   ├── 🐍 blood_test.py
│   │   ├── 🐍 patient.py
│   │   └── 🐍 recommendation.py
│   │
│   ├── 📂 core/                 # Business logic
│   │   ├── 🐍 analyzer.py       # Blood test analysis
│   │   ├── 🐍 advanced_analyzer.py
│   │   ├── 🐍 rule_engine.py    # Pattern matching
│   │   └── 🐍 recommendation_engine.py
│   │
│   ├── 📂 utils/                # Helper utilities
│   │   ├── 🐍 formatter.py      # PDF generation
│   │   ├── 🐍 document_parser.py
│   │   └── 🐍 i18n.py
│   │
│   ├── 📂 gui/                  # PyQt5 interface
│   │   └── 🐍 main_window.py
│   │
│   └── 🐍 main.py               # CLI entry point
│
├── 📂 tests/                    # 39 unit tests
├── 📂 examples/                 # Sample data
├── 📂 i18n/                     # Translations
└── 📂 .github/workflows/        # CI/CD pipelines
```

---

## 🧪 Testing

### Run Tests

```bash
# 📊 Full test suite with coverage
pytest --cov=src --cov-report=html:htmlcov --cov-report=term-missing tests/

# 🎯 Specific test modules
pytest tests/test_analyzer.py -v
pytest tests/test_rule_engine.py -v
```

### Test Coverage

| 📦 Module | 📝 Description | ✅ Status |
|-----------|---------------|-----------|
| Analyzer | Blood test status | ✓ |
| AdvancedAnalyzer | Pattern recognition | ✓ |
| InterpretationEngine | Test interpretation | ✓ |
| RuleEngine | Supplement matching | ✓ |
| RecommendationEngine | Recommendations | ✓ |
| Models | Pydantic validation | ✓ |
| Security | Path & input validation | ✓ |

### 🛡️ Security Features

- 🔒 **Path Traversal Protection** — Validated file paths
- 🧹 **Filename Sanitization** — Safe character handling
- 📏 **File Size Limits** — 50MB maximum
- ✅ **Input Validation** — Pydantic models throughout

---

## 🛠️ Development

### Code Quality Tools

| 🔧 Tool | 📋 Purpose | ⚙️ Config |
|---------|-----------|-----------|
| [Black](https://github.com/psf/black) | Formatting | `pyproject.toml` |
| [Isort](https://pycqa.github.io/isort/) | Import sorting | `pyproject.toml` |
| [Pylint](https://www.pylint.org/) | Static analysis | `.pylintrc` |
| [Pytest](https://pytest.org/) | Testing | `pyproject.toml` |
| [MyPy](http://mypy-lang.org/) | Type checking | `pyproject.toml` |

### Development Workflow

```bash
# 1️⃣ Make changes
# ...

# 2️⃣ Run tests
pytest

# 3️⃣ Check quality
pylint src/ && black --check src/ && isort --check-only src/

# 4️⃣ Commit & push
git commit -m "feat: new feature" && git push
```

---

## 🗺️ Roadmap

<table>
<tr>
<th>Version</th>
<th>Status</th>
<th>Features</th>
</tr>
<tr>
<td><b>2.2</b></td>
<td>🚧 In Progress</td>
<td>
<ul>
<li>🌐 Web Interface (Flask/FastAPI)</li>
<li>🌍 Multi-language Support (English)</li>
<li>📊 Enhanced PDF Reports</li>
</ul>
</td>
</tr>
<tr>
<td><b>2.3</b></td>
<td>📋 Planned</td>
<td>
<ul>
<li>🤖 Machine Learning Recommendations</li>
<li>💊 Drug Interaction Alerts</li>
<li>📱 Mobile Companion App</li>
</ul>
</td>
</tr>
<tr>
<td><b>3.0</b></td>
<td>🔮 Long-term</td>
<td>
<ul>
<li>🏥 HL7 FHIR Integration</li>
<li>🩺 Telemedicine API</li>
<li>🤖 AI Health Chatbot</li>
</ul>
</td>
</tr>
</table>

### 💡 Have Ideas?

- 🐛 [Report Bugs](https://github.com/WielkiKrzych/medical_supplement_advisor/issues)
- 💬 [Request Features](https://github.com/WielkiKrzych/medical_supplement_advisor/issues)
- 🗣️ [Join Discussions](https://github.com/WielkiKrzych/medical_supplement_advisor/discussions)

---

## 🤝 Contributing

We welcome contributions! 

### Quick Contribution Guide

```
🍴 Fork → 🌿 Branch → ✏️ Code → ✅ Test → 📤 Push → 🔀 PR
```

<details>
<summary><b>📋 Detailed Steps</b></summary>

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes following code style
4. **Add** tests for new functionality
5. **Run** tests: `pytest && pylint src/ && black --check src/`
6. **Commit**: `git commit -m "feat: add amazing feature"`
7. **Push**: `git push origin feature/amazing-feature`
8. **Open** a Pull Request

</details>

### Contribution Guidelines

| ✅ Do | ❌ Don't |
|-------|---------|
| Follow PEP 8 | Skip tests |
| Add type hints | Ignore linting |
| Update docs | Leave dead code |
| Write meaningful commits | Force push |

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

<div align="center">

```
MIT License - Free to use, modify, and distribute
```

</div>

---

## 📋 Recent Changes (v2.1.1)

### Code Quality Improvements

This update addresses code review findings to improve security, performance, and maintainability:

#### 🔴 Critical Fixes
- **Security**: Exception details no longer leaked to GUI dialogs in `main_window.py`
- **Security**: Fixed ReDoS-susceptible regex patterns in `document_parser.py`

#### 🟠 High Priority Fixes
- **Data Quality**: Reformatted `supplements.json` with proper indentation for readability
- **Immutability**: Replaced `.sort()` with `sorted()` in `advanced_analyzer.py` and `recommendation_engine.py`
- **Code Style**: Moved inline imports to module level in `advanced_analyzer.py` and `document_parser.py`
- **Error Handling**: Replaced broad `except Exception` with specific exception types
- **Cache Safety**: `DataLoader` now returns deep copies to prevent cache mutation
- **Performance**: Built lookup dicts for O(1) reference range search in `analyzer.py` and `rule_engine.py`

#### 🟡 Medium Priority Fixes
- **Singleton Safety**: Fixed mutable class-level state in `I18n` singleton
- **Logic Fix**: Corrected fallback logic in `_get_priority_display` in `formatter.py`
- **Documentation**: Added explanatory comment for MD5 usage in filename generation

#### 🟢 Low Priority Fixes
- **Cleanup**: Removed unused `AnalysisError` import from `validator.py`

---

## 🔗 Quick Links

## 🔗 Quick Links

<div align="center">

| 📦 Repository | 🐛 Issues | 📥 Pull Requests | 🔄 Actions |
|:-------------:|:---------:|:----------------:|:----------:|
| [GitHub](https://github.com/WielkiKrzych/medical_supplement_advisor) | [Open Issue](https://github.com/WielkiKrzych/medical_supplement_advisor/issues) | [Create PR](https://github.com/WielkiKrzych/medical_supplement_advisor/pulls) | [CI/CD](https://github.com/WielkiKrzych/medical_supplement_advisor/actions) |

</div>

---

<div align="center">

### Made with ❤️ for better health

**⭐ If this project helps you, consider giving it a star! ⭐**

[⬆ Back to Top](#-medical-supplement-advisor)

</div>
