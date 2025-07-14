
# FastAPI Project

A modern, production-ready REST API built with FastAPI, SQLAlchemy, and Alembic, with full support for Docker and robust testing.

---

## 🚀 Features

- **FastAPI** for high-performance APIs
- **JWT authentication** (OAuth2 with password flow)
- **SQLAlchemy ORM** and PostgreSQL support
- **Alembic** for database migrations
- **Dockerized** deployment (`docker-compose`)
- **Unit & integration tests** with pytest
- **Environment variable management** with `.env`
- **Nginx + Gunicorn** (production ready)
- **Blueprint for CI/CD** and scalable deployment

---

## 🗂 Project Structure

```
fastapi-project-main/
├── app/
│   ├── main.py           # FastAPI app entry point
│   ├── models.py         # ORM models
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # Database setup
│   ├── oauth2.py         # JWT/OAuth2 logic
│   ├── config.py         # App settings
│   ├── calculations.py   # Business logic
│   ├── utils.py
│   └── __init__.py
├── tests/                # Pytest tests
├── alembic/              # Database migrations
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose, docker-compose-dev.yml, ...
├── Procfile
├── gunicorn.service
├── nginx/
└── ...
```

---

## ⚡️ Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/fastapi-project-main.git
cd fastapi-project-main/fastapi-project-main
```

### 2. Create a virtualenv & install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables
- Edit `.env` to set DB credentials, JWT secret, etc.

### 4. Initialize the database
- Create the PostgreSQL DB (or use SQLite for local dev)
- Run Alembic migrations:
  ```bash
  alembic upgrade head
  ```

### 5. Run the API (dev)
```bash
uvicorn app.main:app --reload
```
- Open: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐳 Docker & Production

To run the full stack (API + DB + Nginx) with Docker Compose:
```bash
docker-compose up --build
```

- The app will be available at [http://localhost:8000](http://localhost:8000) (or as configured)

---

## 🧪 Testing

```bash
pytest
```

- Tests are in the `tests/` directory
- Use the test database (see `.env` for config)

---

## 🛠️ Migrations

Use Alembic to create and run DB migrations:
```bash
alembic revision --autogenerate -m "Your migration message"
alembic upgrade head
```

---

## 📄 Author

Yves Mboumi  
[LinkedIn](https://linkedin.com/in/yvesmboumi)  
Email: yves.mboumi@gmail.com

---

> Contributions welcome! Fork, PR, and suggestions encouraged.
