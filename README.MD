cat > README.md << 'EOF'
# Commission Calculator API

A FastAPI-based backend system for calculating course sales commissions, generating Excel reports, and storing them in MinIO for secure download.

## Features

- **Student Management** — Add and list students.
- **Course Management** — Add and list courses.
- **Enrollment Management** — Add enrollments (prevents duplicates).
- **Commission Calculation** — Automatically calculate commission based on enrollment date and refund status:
  - **Early Enrollment** (1–15 of month): 20%
  - **Late Enrollment** (16–end of month): 10%
  - **Refunded**: 0%
- **Excel Report Generation** — Creates a detailed commission report.
- **MinIO Integration** — Stores reports in MinIO and generates presigned download URLs.

---

## Tech Stack

- **Backend Framework:** FastAPI
- **Database:** PostgreSQL
- **Object Storage:** MinIO (S3-compatible)
- **Libraries:** Pydantic, boto3, openpyxl, psycopg2

---

## Project Structure

app/
│
├── db.py # Database connection
├── main.py # FastAPI entry point
├── models/ # Database CRUD operations
│ ├── student.py
│ ├── course.py
│ ├── enrollment.py
│
├── schema/ # Pydantic schemas
│ └── report.py
│
├── services/ # Business logic
│ └── report_service.py
│
├── utils/ # Utility functions
│ ├── excel_utils.py
│ └── minio_utils.py
│
└── schema.sql # PostgreSQL table schema


---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/commission-calculator.git
cd commission-calculator

### 2. Create & activate a virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows



3. Install dependencies
pip install -r requirements.txt

4. Setup PostgreSQL
Run the schema file:

psql -U postgres -d your_db_name -f schema.sql


5. Setup MinIO (Docker)

docker run -d --name minio \
  -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=Commission" \
  -v ${HOME}/minio-data:/data \
  quay.io/minio/minio server /data --console-address ":9001"
Access MinIO console: http://localhost:9001
Default login:
Username: minioadmin
Password: Commission


6. Environment Variables
Create a .env file:

DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/your_db_name
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=Commission
MINIO_BUCKET=commission-reports


Running the API

uvicorn app.main:app --reload


API Endpoints
Students
POST /students — Add new student

GET /students — List all students

Courses
POST /courses — Add new course

GET /courses — List all courses

Enrollments
POST /enrolled — Add new enrollment (no duplicates)

GET /commission — Get commission report (JSON)

GET /commission-report/download — Get presigned URL to download Excel report from MinIO

