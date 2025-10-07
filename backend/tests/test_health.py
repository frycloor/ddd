import pytest
from fastapi.testclient import TestClient

try:
    from backend.main import app
except Exception:
    from main import app

client = TestClient(app)

def test_root_health():
    res = client.get('/')
    assert res.status_code == 200
    assert 'status' in res.json()
