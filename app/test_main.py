from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_media():
    response = client.get("/media")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    for item in data:
        assert "id" in item
        assert "title" in item
        assert "type" in item
        assert "genre" in item
        assert "year" in item

def test_get_media_limit():
    response = client.get("/media?limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_get_media_offset():
    first_response = client.get("/media?limit=1&offset=0")
    second_response = client.get("/media?limit=1&offset=1")

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    first_data = first_response.json()
    second_data = second_response.json()

    assert len(first_data) == 1
    assert len(second_data) == 1

    assert first_data[0]["id"] != second_data[0]["id"]

def test_get_media_invalid_limit():
    response = client.get("/media?limit=101")
    assert response.status_code == 422

def test_get_media_invalid_offset():
    response = client.get("/media?offset=-1")
    assert response.status_code == 422

def test_get_media_genre():
    response = client.get("/media?genre=Science%20Fiction")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for item in data:
        assert item["genre"] == "Science Fiction"

def test_get_media_type():
    response = client.get("/media?type=Movie")

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    for item in data:
        assert item["type"] == "Movie"

def test_get_media_title():
    response = client.get("/media?title=The%20Empire%20Strikes%20Back")

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    for item in data:
        assert item["title"] == "The Empire Strikes Back"

def test_get_media_combined_filters():
    response = client.get("/media?type=Movie&genre=Science%20Fiction")

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    for item in data:
        assert item["type"] == "Movie"
        assert item["genre"] == "Science Fiction"

def test_get_media_filter_and_pagination():
    response = client.get(
        "/media?genre=Science%20Fiction&limit=1"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["genre"] == "Science Fiction"