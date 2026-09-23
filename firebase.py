"""Firebase Firestore connection for Schedula.

Credentials are supplied locally through FIREBASE_CREDENTIALS_PATH and are
never committed to the repository.
"""

import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore


DEFAULT_CREDENTIALS_PATH = Path(__file__).resolve().parent.parent / "firebase-service-account.json"
SERVICE_ACCOUNT_FILE = Path(
    os.getenv("FIREBASE_CREDENTIALS_PATH", str(DEFAULT_CREDENTIALS_PATH))
).expanduser()


if not SERVICE_ACCOUNT_FILE.exists():
    raise FileNotFoundError(
        "Firebase credentials not found. Set FIREBASE_CREDENTIALS_PATH to your "
        "local Firebase service-account JSON file. See backend/.env.example."
    )


if not firebase_admin._apps:
    cred = credentials.Certificate(str(SERVICE_ACCOUNT_FILE))
    firebase_admin.initialize_app(cred)


db = firestore.client()
