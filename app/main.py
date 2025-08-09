from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import date
from app.models import student, course, enrollment
from app.services import report_service
from app.schema.report import CommissionReport
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()

# -------- Models --------
class StudentInput(BaseModel):
    name: str
    email: EmailStr

class StudentOutput(StudentInput):
    id: int

class CourseInput(BaseModel):
    name: str
    course_type: str
    base_price: float

class CourseOutput(CourseInput):
    id: int

class EnrollmentInput(BaseModel):
    student_id: int
    course_id: int
    enrolled_at: date
    is_refunded: bool
    refund_date: Optional[date] = None

    @validator("refund_date", always=True)
    def validate_refund(cls, v, values):
        if values.get("is_refunded") and not v:
            raise ValueError("Refund date is required if refunded")
        if v and values.get("enrolled_at") and v <= values["enrolled_at"]:
            raise ValueError("Refund date must be after enrollment date")
        return v

class EnrollmentOutput(EnrollmentInput):
    id: int

# -------- Routes --------
@app.post("/students", response_model=StudentOutput)
def create_student(data: StudentInput):
    try:
        return student.add_student(data.name, data.email)
    except Exception as e:
        err_msg = str(e).lower()
        if "duplicate key" in err_msg or "unique constraint" in err_msg:
            raise HTTPException(status_code=400, detail="Email already exists")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/students", response_model=List[StudentOutput])
def list_students():
    try:
        return student.get_all_students()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/courses", response_model=CourseOutput)
def create_course(data: CourseInput):
    try:
        return course.add_course(data.name, data.course_type, data.base_price)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/courses", response_model=List[CourseOutput])
def list_courses():
    try:
        return course.get_all_courses()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/enrollments", response_model=EnrollmentOutput)
def enroll_student(data: EnrollmentInput):
    try:
        existing = enrollment.get_enrollment_by_student_course(data.student_id, data.course_id)
        if existing:
            raise HTTPException(status_code=400, detail="Student already enrolled in this course")

        return enrollment.add_enrollment(
            data.student_id, data.course_id, data.enrolled_at, data.is_refunded, data.refund_date
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/enrollments", response_model=List[EnrollmentOutput])
def list_enrollments():
    try:
        return enrollment.get_all_enrollments()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/commission", response_model=List[CommissionReport])
def commission_report():
    try:
        return report_service.calculate_commission()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/commission-report/download")
def download_commission_report():
    try:
        url = report_service.get_excel_report_and_upload()
        return JSONResponse(content={"download_url": url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
