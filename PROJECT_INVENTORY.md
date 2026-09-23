# Schedula — GitHub-Safe Project Package

This package contains the application source code and configuration from the supplied project, cleaned for version control.

## Main components
- Android application: `app/`
- Python/FastAPI backend: `backend/`
- Sample timetable data: `sample_data/`

## Excluded from GitHub
- Android/Gradle build output
- Python virtual environment and bytecode caches
- IDE metadata and local SDK configuration
- Firebase service-account credentials
- Local `.env` files and signing credentials

## Firebase setup
Create/download a Firebase service-account JSON file locally and set `FIREBASE_CREDENTIALS_PATH` in `backend/.env` (or as an environment variable). Never commit the credential file.
