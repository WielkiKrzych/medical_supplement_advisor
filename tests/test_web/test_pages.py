import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def test_dashboard_with_data(client_with_data):
    response = client_with_data.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Jan" in response.text
    assert "Kowalski" in response.text


def test_dashboard_without_data(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "brak" in response.text.lower()


def test_chart_data_embedded(client_with_data):
    response = client_with_data.get("/")
    assert "window.analysisData" in response.text
    assert "Krytyczny problem testowy" in response.text


def test_dashboard_has_critical_alerts(client_with_data):
    response = client_with_data.get("/")
    assert response.status_code == 200
    assert "Alerty krytyczne" in response.text
    assert "Krytyczny problem testowy" in response.text


def test_dashboard_has_recommendations(client_with_data):
    response = client_with_data.get("/")
    assert response.status_code == 200
    assert "Podsumowanie rekomendacji" in response.text
    assert "Rekomendacja testowa" in response.text


def test_dashboard_has_patient_header(client_with_data):
    response = client_with_data.get("/")
    assert response.status_code == 200
    assert "2026-04-19" in response.text


def test_dashboard_without_data_no_crash(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Medical Supplement Advisor" in response.text


def test_dashboard_with_rich_data():
    from src.models.test_analysis import (
        ComprehensiveAnalysis,
        TestAnalysis,
        ThyroidInterpretation,
        LipidInterpretation,
        SupplementRecommendation,
        ReferenceRange,
    )
    from src.web.app import create_app
    from fastapi.testclient import TestClient

    analysis = ComprehensiveAnalysis(
        patient_name="Anna",
        patient_surname="Nowak",
        test_date="2026-01-15",
        inflammatory_markers=[
            TestAnalysis(
                name="CRP",
                value=5.2,
                unit="mg/L",
                status="high",
                lab_reference=ReferenceRange(min=0, max=3.0, unit="mg/L"),
                optimal_range=ReferenceRange(min=0, max=1.0, unit="mg/L"),
            )
        ],
        minerals_vitamins=[
            TestAnalysis(
                name="Witamina D",
                value=22.0,
                unit="ng/mL",
                status="low",
                lab_reference=ReferenceRange(min=30, max=100, unit="ng/mL"),
            )
        ],
        electrolytes=[
            TestAnalysis(
                name="Sód",
                value=140,
                unit="mmol/L",
                status="normal",
                lab_reference=ReferenceRange(min=136, max=145, unit="mmol/L"),
            )
        ],
        thyroid=ThyroidInterpretation(
            overall_status="normal",
            tsh_status="normal",
            ft3_percentage=50.0,
            ft4_percentage=45.0,
            recommendations=["Monitoruj tarczycę"],
        ),
        lipids=LipidInterpretation(
            overall_status="elevated",
            total_cholesterol_hdl_ratio=4.5,
            ldl_hdl_ratio=3.0,
            cardiovascular_risk="medium",
            recommendations=["Zwiększ aktywność fizyczną"],
        ),
        all_supplements=[
            SupplementRecommendation(
                supplement_id="vitamin_d3",
                name="Witamina D3",
                dosage="2000 IU/dzień",
                priority="high",
                reason="Niski poziom witaminy D",
            )
        ],
        critical_issues=["Wysokie CRP"],
        recommendations_summary=["Suplementacja witaminą D3"],
    )

    app = create_app(analysis=analysis)
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "Anna" in response.text
    assert "Nowak" in response.text
    assert "CRP" in response.text
    assert "Witamina D" in response.text
    assert "Sód" in response.text
    assert "Tarczyca" in response.text
    assert "Lipidogram" in response.text
    assert "Witamina D3" in response.text
    assert "Wysokie CRP" in response.text
    assert "2000 IU" in response.text
