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

def test_create_and_return_loan():
    response = client.post(
        "/loans",
        json={
            "copy_id": 2,
            "user_id": 1
        }
    )

    assert response.status_code == 201

    loan = response.json()

    assert loan["copy_id"] == 2
    assert loan["user_id"] == 1

    loan_id = loan["id"]

    return_response = client.post(f"/loans/{loan_id}/return")

    assert return_response.status_code == 200

def test_cannot_checkout_checked_out_copy():
    first_response = client.post(
        "/loans",
        json={
            "copy_id": 2,
            "user_id": 1
        }
    )

    assert first_response.status_code == 201

    loan_id = first_response.json()["id"]

    second_response = client.post(
        "/loans",
        json={
            "copy_id": 2,
            "user_id": 1
        }
    )

    assert second_response.status_code == 409

    return_response = client.post(f"/loans/{loan_id}/return")

    assert return_response.status_code == 200

def test_create_loan_invalid_copy():
    response = client.post(
        "/loans",
        json={
            "copy_id": 9999,
            "user_id": 1
        }
    )

    assert response.status_code == 404

def test_create_loan_invalid_user():
    response = client.post(
        "/loans",
        json={
            "copy_id": 2,
            "user_id": 9999
        }
    )

    assert response.status_code == 404

def test_cannot_return_loan_twice():
    response = client.post(
        "/loans",
        json={
            "copy_id": 2,
            "user_id": 1
        }
    )

    assert response.status_code == 201

    loan_id = response.json()["id"]

    first_return = client.post(f"/loans/{loan_id}/return")

    assert first_return.status_code == 200

    second_return = client.post(f"/loans/{loan_id}/return")

    assert second_return.status_code == 404

def test_return_nonexistent_loan():
    response = client.post("/loans/9999/return")

    assert response.status_code == 404

def test_get_loans():
    response = client.get("/loans")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    for loan in data:
        assert "id" in loan
        assert "title" in loan
        assert "format" in loan
        assert "name" in loan
        assert "checked_out_at" in loan
        assert "returned_at" in loan

def test_get_active_loans():
    response = client.get("/loans/active")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for loan in data:
        assert "id" in loan
        assert "title" in loan
        assert "format" in loan
        assert "name" in loan
        assert "checked_out_at" in loan

def test_active_loan_lifecycle():
    response = client.post(
        "/loans",
        json={
            "copy_id": 2,
            "user_id": 1
        }
    )

    assert response.status_code == 201

    loan_id = response.json()["id"]

    active_response = client.get("/loans/active")

    assert active_response.status_code == 200

    active_loans = active_response.json()

    assert any(loan["id"] == loan_id for loan in active_loans)

    return_response = client.post(f"/loans/{loan_id}/return")

    assert return_response.status_code == 200

    active_response = client.get("/loans/active")

    assert active_response.status_code == 200

    active_loans = active_response.json()

    assert all(loan["id"] != loan_id for loan in active_loans)