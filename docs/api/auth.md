# Authentication API

Endpoints for registering users and logging in. All paths are relative to the base URL
(`http://127.0.0.1:8000` in local dev).

| Method | Path | Auth required | Description |
|--------|------|---------------|-------------|
| `POST` | `/auth/register` | No | Create a new user account |
| `POST` | `/auth/login` | No | Authenticate and receive a JWT access token |

---

## POST `/auth/register`

Creates a new user account.

### Request body

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | yes | Display name |
| `email` | string | yes | Must be unique |
| `password` | string | yes | Plaintext; hashed server-side before storage |

```json
{
  "name": "Nuwan",
  "email": "nuwan@example.com",
  "password": "secret123"
}
```

### Success response — `201 Created`

| Field | Type | Description |
|-------|------|-------------|
| `id` | string (UUID) | Unique user id |
| `name` | string | Display name |
| `email` | string | User email |
| `password` | string | **Hashed** password. ⚠️ Currently returned but should be ignored by the frontend (will be removed). |
| `created_at` | string (ISO 8601) | Creation timestamp (UTC) |
| `updated_at` | string (ISO 8601) | Last update timestamp (UTC) |
| `is_active` | boolean | Whether the account is active (default `true`) |
| `is_superuser` | boolean | Admin flag (default `false`) |
| `is_feeder` | boolean | Data-feeder role flag (default `false`) |
| `is_verified` | boolean | Email-verified flag (default `false`) |
| `role` | string | One of `admin`, `user`, `feeder` (default `"user"`) |

```json
{
  "id": "aa3a21c2-f558-490b-8afd-b1c4fe098b75",
  "name": "Nuwan",
  "email": "nuwan@example.com",
  "password": "$2b$12$....",
  "created_at": "2026-06-13T07:44:00",
  "updated_at": "2026-06-13T07:44:00",
  "is_active": true,
  "is_superuser": false,
  "is_feeder": false,
  "is_verified": false,
  "role": "user"
}
```

### Error responses

| Status | `detail` | When |
|--------|----------|------|
| `400` | `Email already registered` | The email is already in use |
| `400` | `Email, password and name are required` | A field was sent but empty (`""`) |
| `422` | _validation list_ | A required field is missing or has the wrong type |

### Examples

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Nuwan","email":"nuwan@example.com","password":"secret123"}'
```

```ts
const res = await fetch("http://127.0.0.1:8000/auth/register", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name, email, password }),
});
if (!res.ok) throw new Error((await res.json()).detail);
const user = await res.json();
```

---

## POST `/auth/login`

Authenticates a user and returns a JWT access token.

### Request body

| Field | Type | Required |
|-------|------|----------|
| `email` | string | yes |
| `password` | string | yes |

```json
{
  "email": "nuwan@example.com",
  "password": "secret123"
}
```

### Success response — `200 OK`

| Field | Type | Description |
|-------|------|-------------|
| `access_token` | string | Signed JWT |
| `token_type` | string | Always `"bearer"` |

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVC9.eyJzdWIiOiJhYTNh...",
  "token_type": "bearer"
}
```

### Error responses

| Status | `detail` | When |
|--------|----------|------|
| `401` | `Invalid email or password` | Unknown email **or** wrong password (intentionally identical to avoid leaking which emails exist) |
| `403` | `Account is inactive` | The account exists but `is_active` is `false` |
| `400` | `Email and password are required` | A field was sent but empty (`""`) |
| `422` | _validation list_ | A required field is missing or has the wrong type |

### Examples

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"nuwan@example.com","password":"secret123"}'
```

```ts
const res = await fetch("http://127.0.0.1:8000/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ email, password }),
});
if (!res.ok) throw new Error((await res.json()).detail);
const { access_token } = await res.json();
localStorage.setItem("access_token", access_token);
```

---

## Using the token

Send the token on subsequent requests to protected endpoints:

```
Authorization: Bearer <access_token>
```

### Token details

| Property | Value |
|----------|-------|
| Type | JWT |
| Algorithm | `HS256` |
| Expiry | 60 minutes from issue |
| `sub` claim | The user's `id` |

> There is no refresh-token endpoint yet, so once a token expires the user must log in again.
