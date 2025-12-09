from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!!!"}


def test_square_ok():
    response = client.get("/square/3")
    assert response.status_code == 200
    assert response.json() == {"result": 9}


def test_square_too_large():
    """Quando o valor é muito grande, o endpoint deve rejeitar a requisição."""

    response = client.get("/square/10001")
    assert response.status_code == 400
    assert response.json()["detail"] == "x is too large"


def test_double_without_validation():
    """Uso simples de query param sem validação extra."""

    response = client.get("/double", params={"x": 8})
    assert response.status_code == 200
    assert response.json() == {"result": 16}


def test_double_validated_in_range():
    response = client.get("/double", params={"x": 10, "validated": True})
    assert response.status_code == 200
    assert response.json() == {"result": 20}


def test_double_validated_out_of_range():
    response = client.get("/double", params={"x": 101, "validated": True})
    assert response.status_code == 422
    assert response.json()["detail"] == "x out of allowed range (-100, 100)"


def test_stats_basic():
    response = client.get(
        "/stats", params=[("numbers", 1), ("numbers", 2), ("numbers", 3)]
    )
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 3
    assert body["total"] == 6
    assert body["average"] == 2
    assert body["min"] == 1
    assert body["max"] == 3


def test_stats_empty_list():
    """Quando a lista é vazia, esperamos um erro 422."""

    response = client.get("/stats")
    assert response.status_code == 422
    body = response.json()
    assert body["detail"][0]["loc"] == ["query", "numbers"]
    assert body["detail"][0]["msg"] == "Field required"
