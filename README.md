# Campus Cash Control

Campus Cash Control is a full stack financial tracking platform designed for university audit and expense oversight workflows. It provides a centralized place to upload departmental financial data, manage departments, control user access, and generate filtered reports for review.

Live: https://main.dl7euuqn926l2.amplifyapp.com/

## Project Purpose

This project helps institutions improve financial transparency by:

- standardizing how departmental expense and revenue data is submitted
- reducing manual data consolidation effort during audits
- enabling quick reporting by department, month, and year
- supporting secure user authentication for controlled access

## What This Project Does

The system is split into two applications:

- Frontend: Vue 3 interface for login, dashboard, departments, upload, reports, and user access views
- Backend: Django REST API with PostgreSQL integration, JWT authentication, and data processing endpoints

Core capabilities:

- JWT based authentication and account signup
- Department listing and department management operations
- Upload of financial files in CSV, XLSX, XLSM, and XLS formats
- Validation of required data columns before insert
- Report generation with filters for department, month, and year
- Listing authenticated active users for access management workflows

## Tech Stack

- Frontend: Vue 3, Vue Router, Axios, Element Plus, Bootstrap
- Backend: Django 5, Django REST Framework, Simple JWT
- Data handling: Pandas, OpenPyXL, xlrd
- Database: PostgreSQL
- Deployment: AWS Amplify (frontend) and Render (backend)

## Repository Structure

- `campuscashcontrolf/`: Vue frontend application
- `campuscashcontrolb/`: Django backend application
- `amplify.yml`: Amplify build configuration
- `render.yaml`: Render service and database configuration

## Installation and Local Setup

### Prerequisites

- Python 3.10 or newer
- Node.js 18 or newer and npm
- PostgreSQL

### 1) Clone the repository

```bash
git clone https://github.com/VivekChoudhary77/CS-542-CampusCashControl.git
cd CS-542-CampusCashControl
```

### 2) Setup and run backend

```bash
cd campuscashcontrolb
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3) Setup and run frontend

Open a second terminal:

```bash
cd campuscashcontrolf
npm install
npm run serve
```

### 4) Configure frontend API base URL (optional for non default backend host)

Create a `.env` file in `campuscashcontrolf/`:

```bash
VUE_APP_API_BASE_URL=http://localhost:8000
```

## Quick Guide

1. Open the app and sign in with a valid account.
2. Go to Departments to review active departments or perform department management actions.
3. Go to Upload and submit a finance file with required columns: `Items` and `Revenue`.
4. Go to Reports and filter data by department, month, and year.
5. Use User Access to view authenticated active users.

## Main API Endpoints

- `POST /api/signup/`
- `POST /api/token/`
- `POST /api/token/refresh/`
- `GET /api/departments/`
- `POST /api/manage-department/`
- `GET /api/departments/active/`
- `POST /api/upload/`
- `GET /api/reports/`
- `GET /api/auth-users/`

## Notes for Auditing Workflow

- Upload validation ensures required fields are present before data is written.
- Report filters support both broad and targeted audit views.
- Department status controls can help keep reporting aligned with active units.

## Future Improvements

- role based permission levels beyond basic authentication
- richer dashboard analytics and trend visualizations
- automated data quality checks and exception reporting
- audit trail logging for critical administrative actions
