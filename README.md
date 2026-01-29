# Medical Supplement Advisor

Application for generating supplement recommendations based on blood test results.

## Installation

```bash
cd medical-supplement-advisor
pip install -r requirements.txt
```

## Usage

```bash
python src/main.py
```

## Project Structure

```
medical-supplement-advisor/
├── data/                          # Reference data (JSON)
│   ├── reference_ranges.json      # Blood test reference ranges
│   ├── supplements.json            # Supplement list with dosages
│   ├── timing_rules.json           # Timing rules
│   └── dosage_rules.json           # Dosage rules for conditions
├── src/
│   ├── models/                     # Data models
│   ├── core/                       # Business logic
│   │   ├── analyzer.py              # Blood test analysis
│   │   ├── rule_engine.py          # Rule matching engine
│   │   └── recommendation_engine.py # Recommendation generation
│   ├── utils/                      # Utilities
│   │   ├── exceptions.py            # Custom exception classes
│   │   ├── validator.py            # Data validation
│   │   ├── data_loader.py         # JSON data loading
│   │   ├── formatter.py            # PDF report generation
│   │   └── json_parser.py          # JSON input parsing
│   └── main.py                     # Entry point
├── tests/                          # Unit tests
│   ├── test_analyzer.py          # Analyzer tests
│   ├── test_rule_engine.py       # Rule engine tests
│   └── test_recommendation_engine.py # Recommendation engine tests
└── examples/                       # Sample data
```

## Input

Blood test results with patient information:
- Patient data: name, surname, age, medical conditions
- Blood tests: test name, value, unit

## Output

PDF report with:
- Supplement recommendations
- Dosage for each supplement
- Timing (when to take)
- Priority level

## Quality & Development Tools

The project uses modern Python development tools to maintain code quality:

### Code Quality
- **Pylint**: Static code analysis and error detection
  - Configured in `.pylintrc`
  - Runs in CI/CD pipeline
  - Score threshold: 9.0
- **Black**: Code formatter (PEP 8 compliant)
  - Configured in `pyproject.toml`
  - 100 character line length
  - Runs in CI/CD pipeline
- **Isort**: Import organizer
  - Configured in `pyproject.toml`
  - Compatible with Black formatting
  - Runs in CI/CD pipeline

### Testing
- **Pytest**: Testing framework
  - Parametrized test cases
  - Fixture-based test setup
  - Coverage reporting with `pytest-cov`
  - HTML coverage reports

### Continuous Integration
- **GitHub Actions**: Automated CI/CD pipeline
  - Runs on push and pull requests
  - Multi-version Python testing (3.11, 3.12, 3.13)
  - Automated linting and formatting checks
  - Coverage uploads to Codecov

### Documentation
- **Docstrings**: Public API methods documented
- **Type Hints**: Full type annotation coverage
- **PEP 8**: Code style compliance

## Testing

### Running Tests

```bash
# Run all tests with coverage
pytest --cov=src --cov-report=html:htmlcov --cov-report=term-missing tests/

# Run specific test modules
pytest tests/test_analyzer.py -v
pytest tests/test_rule_engine.py -v
pytest tests/test_recommendation_engine.py -v
```

### Test Coverage

The project has comprehensive test coverage for core business logic:

- **Analyzer** (`src/core/analyzer.py`): Tests blood test status determination
- **RuleEngine** (`src/core/rule_engine.py`): Tests rule matching and application
- **RecommendationEngine** (`src/core/recommendation_engine.py`): Tests recommendation generation
- **Models** (`tests/test_analyzer.py`): Tests Pydantic data models

Coverage reports are generated in `htmlcov/` directory and uploaded to CI.

## Code Quality Improvements

Recent improvements to codebase:

1. **Custom Exception Classes**: Added dedicated exception types for better error handling
   - `ValidationError`: Data structure validation errors
   - `DataLoaderError`: JSON file loading errors
   - `RuleEngineError`: Rule engine errors
   - `AnalysisError`: Blood test analysis errors

2. **Enhanced Validation**: Refactored Validator to raise exceptions instead of returning booleans
   - Proper error propagation to callers
   - Clear error messages with context

3. **Code Duplication Eliminated**: Single source of truth for priority ordering
   - Added `PRIORITY_ORDER` to `config.py`
   - Imported in both `RuleEngine` and `RecommendationEngine`
   - Eliminated duplicate dictionary definitions

4. **Type Safety**: Optional parameters properly typed
   - Exception fields use `str | None` union types
   - Better IDE support and type checking

## Architecture

The application follows a clean layered architecture:

- **Models**: Pydantic data models with automatic validation
- **Core**: Business logic separated into specialized engines
  - Analyzer: Blood test status determination
  - RuleEngine: Pattern matching for supplements
  - RecommendationEngine: Coordinated recommendation generation
- **Utils**: Helper functions for I/O, validation, formatting
- **Entry Points**: CLI (`src/main.py`) and GUI (`src/gui/app.py`)

## Development Workflow

1. Make changes to code
2. Run local tests: `pytest`
3. Check linting: `pylint src/`
4. Check formatting: `black --check src/` && `isort --check-only src/`
5. Commit changes with descriptive message
6. Push to trigger CI/CD pipeline

All quality checks run automatically in GitHub Actions.
