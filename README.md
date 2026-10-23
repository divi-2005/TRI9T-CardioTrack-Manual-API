# CardioTrack Manual API

## 1. Project Overview

CardioTrack Manual API is a Python-based REST API built using FastAPI. It allows users to upload PDF manuals, extract sections, store manual information, and compare different versions of manuals to identify changes.

## 2. Objectives

- Upload and process PDF manuals.
- Extract text and sections from manuals.
- Store manual information and version details.
- Compare two manual versions.
- Provide API endpoints for accessing manual data.
- Test the application using automated tests.

## 3. Technologies Used

- Python
- FastAPI
- Uvicorn
- PDF parsing libraries
- Pytest
- Swagger UI

## 4. Project Features

1. **Manual Ingestion:** Upload PDF manuals through the API.
2. **Manual Listing:** Retrieve the available manuals.
3. **Section Extraction:** View the sections extracted from a manual.
4. **Version Comparison:** Compare two manual versions and view their differences.
5. **Health Check:** Check whether the API is running.

## 5. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check the API welcome response |
| GET | `/health` | Check API health |
| POST | `/manuals/ingest` | Upload and process a PDF manual |
| GET | `/manuals` | List available manuals |
| GET | `/manuals/{manual_id}/sections` | Retrieve manual sections |
| GET | `/manuals/compare/{old_id}/{new_id}` | Compare two manual versions |

## 6. Installation and Execution

### Step 1: Open the project folder

Open the `TRI9T DRIVE` folder in Visual Studio Code.

### Step 2: Activate the virtual environment

On Windows PowerShell, run:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

If a `requirements.txt` file is available, run:

```powershell
pip install -r requirements.txt
```

### Step 4: Start the server

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Step 5: Open the API documentation

Open the following URL in your browser:

http://127.0.0.1:8000/docs

Use Swagger UI to upload manuals and test the available endpoints.

## 7. Testing

Run the automated tests using:

```powershell
python -m pytest -q
```

The current test result is **6 passed**.

## 8. Conclusion

CardioTrack Manual API demonstrates how FastAPI can be used to build a REST API for processing PDF manuals, extracting sections, managing manual versions, and comparing changes. The application provides interactive API documentation and automated tests to support development and verification.
