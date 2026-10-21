# FastAPI Task Manager API

A clean, production-ready REST API for task management built with FastAPI, PostgreSQL, and SQLAlchemy. Features JWT authentication, user-scoped task management, and background email notifications.

---

## Features

- **User Authentication**: Secure user registration, password hashing via Argon2 (`pwdlib`), and JWT-based authentication.
- **Task Management (CRUD)**: Create, read, update, and delete tasks isolated to the authenticated user.
- **Background Tasks**: Asynchronous email notifications sent on account registration using `fastapi-mail`.
- **Relational Database**: PostgreSQL with SQLAlchemy ORM and automatic schema creation.
- **Interactive Documentation**: Auto-generated Swagger UI and ReDoc.

---

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) & [Psycopg 3](https://www.psycopg.org/)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **Authentication**: [PyJWT](https://pyjwt.readthedocs.io/) & [pwdlib](https://frankie567.github.io/pwdlib/)
- **Email**: [FastAPI-Mail](https://sabuhish.github.io/fastapi-mail/)

---

## Project Structure

```text
fastapi-task-manager/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app definition & router registration
│   ├── settings.py              # Configuration & environment variables
│   ├── database.py              # Database connection & session setup
│   ├── models.py                # SQLAlchemy models (User, Task)
│   ├── schemas.py               # Pydantic schemas for request/response validation
│   ├── crud.py                  # Database operations & password hashing
│   ├── auth.py                  # Authentication dependencies (JWT verification)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── tasks.py             # Task endpoints (/tasks)
│   │   └── users.py             # User endpoints (/users)
│   └── utils/
│       ├── __init__.py
│       └── mail.py              # Email dispatch utility
├── scripts/
│   ├── create_tables.py         # Database table initialization script
│   └── test_db.py               # Database connectivity test script
├── .env.example                 # Example environment variables template
├── .gitignore                   # Git ignore configuration
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

---

## Getting Started

### 1. Prerequisites

- Python 3.10+
- PostgreSQL database

### 2. Clone Repository & Setup Virtual Environment

```bash
git clone https://github.com/YOUR_USERNAME/fastapi-task-manager.git
cd fastapi-task-manager

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Description | Example |
| :--- | :--- | :--- |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg://user:pass@localhost:5432/task_db` |
| `JWT_SECRET_KEY` | Secret key used for signing JWT tokens | `your-secure-random-key` |
| `JWT_ALGORITHM` | Algorithm for JWT tokens | `HS256` |
| `JWT_EXPIRE_MINUTES` | Token expiry duration in minutes | `30` |
| `MAIL_USERNAME` | SMTP email address | `user@example.com` |
| `MAIL_PASSWORD` | SMTP app password | `app-password` |
| `MAIL_FROM` | Sender email address | `user@example.com` |
| `MAIL_PORT` | SMTP port | `587` |
| `MAIL_SERVER` | SMTP host | `smtp.gmail.com` |

### 5. Initialize Database

Run the table creation script to create tables (`users`, `tasks`) in PostgreSQL:

```bash
python scripts/create_tables.py
```

To test connectivity:

```bash
python scripts/test_db.py
```

### 6. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API Root**: `http://127.0.0.1:8000/`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **Alternative ReDoc**: `http://127.0.0.1:8000/redoc`

---

## API Endpoints

### General
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | API status message | No |

### Authentication & Users
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/users/register` | Register a new user and send welcome email | No |
| `POST` | `/users/login` | Authenticate user credentials & receive JWT token | No |
| `GET` | `/users/is-auth` | Retrieve authenticated user profile | Yes (Bearer) |

### Tasks
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/tasks/` | Create a new task | Yes (Bearer) |
| `GET` | `/tasks/` | List all tasks of the logged-in user | Yes (Bearer) |
| `GET` | `/tasks/{task_id}` | Retrieve a specific task by ID | Yes (Bearer) |
| `PUT` | `/tasks/{task_id}` | Update task title, description, or completion status | Yes (Bearer) |
| `DELETE` | `/tasks/{task_id}` | Delete a task | Yes (Bearer) |

---

## License

This project is open-source and available under the [MIT License](LICENSE).