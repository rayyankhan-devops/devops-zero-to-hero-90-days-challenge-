# SecureVault Platform

SecureVault is a Flask-based practice project for configuration, service separation, and secure application structure.

It is split into three Flask services:

- Auth service
- Notes service
- Tasks service

The frontend is a static SPA and the services share common helpers in `shared/`.

## Repository Layout

- `services/auth` contains registration, login, profile, JWT handling, and the auth database model.
- `services/notes` contains note CRUD and ownership checks.
- `services/tasks` contains task CRUD, dashboard stats, and validation rules.
- `shared` contains configuration, database, health, and security helpers.
- `frontend` contains the SPA.

## Environment Variables

Copy `.env.example` to `.env` and adjust values for your local machine.

Required variables:

- `SECRET_KEY` for JWT signing
- `PASSWORD_SALT` for password hashing
- `DATABASE_URL` for the database connection string
- `CORS_ORIGINS` for allowed browser origins

Useful tuning variables:

- `APP_ENV`
- `JWT_EXPIRATION_HOURS`
- `LOG_LEVEL`
- `MAX_CONTENT_LENGTH`
- `API_VERSION`

## Running Locally

Install the Python dependencies for the service you want to run and start it directly with Python.

Example:

```bash
cd services/auth
python app.py
```

Repeat the same pattern for `services/notes` and `services/tasks`.

## Service Endpoints

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/profile`
- `PUT /api/auth/profile`
- `GET /api/notes/`
- `POST /api/notes/`
- `GET /api/notes/{id}`
- `PUT /api/notes/{id}`
- `DELETE /api/notes/{id}`
- `GET /api/tasks/`
- `GET /api/tasks/stats`
- `POST /api/tasks/`
- `GET /api/tasks/{id}`
- `PUT /api/tasks/{id}`
- `DELETE /api/tasks/{id}`

## Tests

Run the focused service tests with:

```bash
pytest services/auth/tests/test_auth_api.py services/notes/tests/test_notes_api.py services/tasks/tests/test_tasks_api.py -q
```

## Notes

- `shared/security.py` centralizes JWT and password utilities so the services stay consistent.
- `sonar-project.properties` scans the service, shared, and frontend code.

This project is intentionally structured for practicing configuration-driven development and service separation.