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
