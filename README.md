# Schedula Python Backend API & Conflict Engine

FastAPI-powered timetable clash detection, room optimization, and spreadsheet processing engine.

## Features
- **Deterministic Conflict Detection**: Instant pairwise interval overlap detection for Instructor clashes, Room clashes, Student Batch collisions, Capacity overflows, and time validity errors.
- **Smart Conflict Resolver**: Proposes vacancy-verified rooms and non-conflicting time slots across curriculum schedules.
- **Multi-Format Excel & CSV Engine**: Accepts Excel (`.xlsx`, `.xls`) and CSV spreadsheets with fuzzy header normalization, and exports color-coded audit workbooks.
- **RESTful OpenAPI / Swagger**: Interactive API docs available at `/docs` and ReDoc at `/redoc`.

## Quick Start

### Running Locally with Python
```bash
cd backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Running with Docker & Compose
```bash
cd backend
docker-compose up --build
```

### Running Unit Tests
```bash
python3 -m unittest discover -s backend/tests -t backend
```

## API Specification

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Service health and engine readiness |
| `GET` | `/api/v1/timetable/sample-data` | Retrieve sample academic timetable with test clashes |
| `POST` | `/api/v1/timetable/detect-conflicts` | Detect collisions across a list of scheduled slots |
| `POST` | `/api/v1/timetable/resolve-conflicts` | Generate clash resolution recommendations |
| `POST` | `/api/v1/timetable/upload` | Upload `.xlsx`, `.xls`, or `.csv` timetable file |
| `GET` | `/api/v1/timetable/template` | Download standard CSV spreadsheet template |
| `POST` | `/api/v1/timetable/export-excel` | Generate formatted multi-sheet Excel audit report |
