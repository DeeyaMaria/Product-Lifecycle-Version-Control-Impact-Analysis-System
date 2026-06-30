# VersionForge – Product Lifecycle Version Control & Impact Analysis System

VersionForge is a web-based application that applies version control concepts to product requirements. It enables users to manage product versions, track changes, compare versions, approve/reject updates, perform impact analysis, and roll back to previous versions.

## Tech Stack

- FastAPI
- MySQL
- SQLAlchemy
- HTML, CSS, JavaScript
- Bootstrap

## Features

- Product Management
- Requirement Management
- Version Control
- Change Tracking
- Version Comparison
- Approval Workflow
- Rollback
- JWT Authentication

## Running the Project

### Prerequisites
- Python 3.x
- MySQL
- VS Code Live Server (optional)

### Installation

```bash
pip install -r requirements.txt
```

Import the provided SQL database into MySQL.

### Start the Backend Services

```bash
uvicorn version_main:app --reload --port 8000
```

```bash
uvicorn requirement_main:app --reload --port 8001
```

```bash
uvicorn auth_main:app --reload --port 8002
```

### Run the Frontend

Open `frontend/login.html` using Live Server or your browser.

## API URLs

- Version Service: http://127.0.0.1:8000
- Requirement Service: http://127.0.0.1:8001
- Authentication & Product Service: http://127.0.0.1:8002
