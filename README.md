# Schedula

**Schedula** is a full-stack timetable management system designed to simplify timetable creation, management, and conflict handling.

The project consists of an **Android application** and a **FastAPI backend**, with features for timetable processing, conflict detection, conflict resolution, and Excel/CSV data handling.

## 🚀 Features

* 📅 Timetable management
* ⚠️ Automatic timetable conflict detection
* 🔄 Conflict resolution
* 📊 Excel/CSV timetable processing
* 📱 Android application built with Kotlin and Jetpack Compose
* ⚡ FastAPI backend
* 🔥 Firebase/Firestore integration
* 📄 Excel template generation and export
* 🧪 Backend and application testing

## 🏗️ Project Structure

```text
Schedula/
├── app/                 # Android application
├── backend/             # FastAPI backend and scheduling engine
├── sample_data/         # Sample timetable data
├── README.md
└── ...
```

## 📱 Android Application

The Android application is developed using:

* Kotlin
* Jetpack Compose
* Android Studio

To run the application:

1. Clone the repository.
2. Open the project in **Android Studio**.
3. Allow Gradle to sync.
4. Configure the required backend/Firebase settings.
5. Run the application on an emulator or Android device.

The application can use its local conflict-processing functionality and can communicate with the FastAPI backend.

## ⚙️ Backend

The backend is developed using **FastAPI** and provides APIs for timetable processing and conflict management.

Detailed backend setup instructions are available in:

[`backend/README.md`](backend/README.md)

### Main API Endpoints

| Method | Endpoint                              | Purpose                            |
| ------ | ------------------------------------- | ---------------------------------- |
| GET    | `/health`                             | Check backend status               |
| GET    | `/docs`                               | Open FastAPI Swagger documentation |
| GET    | `/api/v1/timetable/sample-data`       | Retrieve sample timetable data     |
| POST   | `/api/v1/timetable/detect-conflicts`  | Detect timetable conflicts         |
| POST   | `/api/v1/timetable/resolve-conflicts` | Resolve timetable conflicts        |
| POST   | `/api/v1/timetable/upload`            | Upload timetable data              |
| GET    | `/api/v1/timetable/template`          | Get timetable template             |
| POST   | `/api/v1/timetable/export-excel`      | Export timetable data to Excel     |

## 🔥 Firebase Configuration

Schedula uses the **Firebase Admin SDK** for Firestore integration.

For security, Firebase service-account credentials are **not included in this repository**.

To configure Firebase locally:

1. Create/download your Firebase service-account JSON from your Firebase/Google Cloud project.
2. Store the credential file outside the repository or in a Git-ignored location.
3. Copy:

```text
backend/.env.example
```

to:

```text
backend/.env
```

4. Set the `FIREBASE_CREDENTIALS_PATH` variable to the location of your credential file.
5. Install the backend dependencies.
6. Start the FastAPI server.

> **Security:** Never commit Firebase service-account JSON files, API secrets, `.env` files, or other private credentials to GitHub.

## 🧪 Testing

The project includes tests for the application and backend components.

Refer to the backend documentation for the available testing and API instructions.

## 🛠️ Technologies Used

**Frontend / Mobile**

* Kotlin
* Jetpack Compose
* Android Studio

**Backend**

* Python
* FastAPI
* Uvicorn

**Database / Cloud**

* Firebase
* Firestore

**Data Processing**

* Excel
* CSV

**Development Tools**

* Git
* GitHub
* Postman
* Android Studio

## 🎯 Project Goal

Schedula aims to provide a practical system for managing academic timetables while reducing manual effort in identifying and handling scheduling conflicts.

## 🔐 Security

Sensitive credentials and local configuration files are excluded from the repository.

If you are setting up the project locally, follow the configuration instructions provided in the backend documentation.

## 📌 Project Status

This project is under active development. Features and implementation details may be updated as the project evolves.
