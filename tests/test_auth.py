def make_payload(**overrides):
    """Default valid registration payload, with optional field overrides."""
    payload = {
        "name": "Nuwan",
        "email": "nuwan@example.com",
        "password": "secret123",
    }
    payload.update(overrides)
    return payload


# --- /auth/register -------------------------------------------------------


def test_register_success(client):
    response = client.post("/auth/register", json=make_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "nuwan@example.com"
    assert body["name"] == "Nuwan"
    assert "id" in body
    # The raw password must never be returned to the client.
    assert body.get("password") != "secret123"


def test_register_duplicate_email_is_rejected(client):
    client.post("/auth/register", json=make_payload())

    response = client.post("/auth/register", json=make_payload(name="Someone Else"))

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_register_missing_field_is_unprocessable(client):
    # "name" is required, so omitting it triggers FastAPI/Pydantic validation.
    response = client.post(
        "/auth/register",
        json={"email": "x@example.com", "password": "secret123"},
    )

    assert response.status_code == 422


# --- /auth/login ----------------------------------------------------------


def test_login_success_returns_token(client):
    client.post("/auth/register", json=make_payload())

    response = client.post(
        "/auth/login",
        json={"email": "nuwan@example.com", "password": "secret123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_wrong_password_is_unauthorized(client):
    client.post("/auth/register", json=make_payload())

    response = client.post(
        "/auth/login",
        json={"email": "nuwan@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_unknown_email_is_unauthorized(client):
    response = client.post(
        "/auth/login",
        json={"email": "ghost@example.com", "password": "whatever"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
