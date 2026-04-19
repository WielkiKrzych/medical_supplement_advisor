import sys
from pathlib import Path

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
from fastapi.testclient import TestClient
from src.web.app import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


@pytest.fixture
def sample_analysis():
    from src.models.test_analysis import (
        ComprehensiveAnalysis,
    )

    return ComprehensiveAnalysis(
        patient_name="Jan",
        patient_surname="Kowalski",
        test_date="2026-04-19",
        morphology=None,
        inflammatory_markers=[],
        minerals_vitamins=[],
        electrolytes=[],
        thyroid=None,
        glucose_insulin=None,
        lipids=None,
        liver=None,
        hormones=None,
        all_supplements=[],
        critical_issues=["Krytyczny problem testowy"],
        recommendations_summary=["Rekomendacja testowa"],
    )


@pytest.fixture
def client_with_data(sample_analysis):
    app = create_app(analysis=sample_analysis)
    return TestClient(app)
