# API Documentation

This directory holds the API reference used by the frontend to integrate with the backend.

Add one Markdown file per feature/domain (e.g. `auth.md`, `companies.md`, `portfolio.md`).

## Index

| Domain | File | Endpoints |
|--------|------|-----------|
| Authentication | [`auth.md`](./auth.md) | `POST /auth/register`, `POST /auth/login` |

## Conventions

- **Base URL (local dev):** `http://127.0.0.1:8000`
- **Content type:** All request and response bodies are JSON (`Content-Type: application/json`).
- **Authentication:** Protected endpoints expect a JWT in the header:
  `Authorization: Bearer <access_token>`
- **Timestamps:** ISO 8601 strings in UTC (e.g. `2026-06-13T07:44:00`).
- **IDs:** UUID v4 strings.

## Common error format

FastAPI returns errors in this shape:

```json
{ "detail": "Human readable message" }
```

Validation errors (missing/wrong-typed fields) return HTTP `422` with a list:

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "email"],
      "msg": "Field required",
      "input": { "name": "Nuwan", "password": "secret123" }
    }
  ]
}
```

## Interactive docs

While the server is running, auto-generated docs are also available at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`
