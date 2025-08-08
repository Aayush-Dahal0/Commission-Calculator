from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import date
from app.models import student, course, enrollment
from app.services import report_service
from app.schema.report import CommissionReport
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

class StudentInput(BaseModel):
    name: str
    email: EmailStr

class CourseInput(BaseModel):
    name: str
    course_type: str
    base_price: float

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

@app.post("/students")
def create_student(data: StudentInput):
    try:
        return student.add_student(data.name, data.email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@app.post("/courses")
def create_course(data: CourseInput):
    try:
        return course.add_course(data.name, data.course_type, data.base_price)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/enrolled")
def enroll_student(data: EnrollmentInput):
    try:
        return enrollment.add_enrollment(
            data.student_id, data.course_id, data.enrolled_at, data.is_refunded, data.refund_date
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/commission", response_model=List[CommissionReport])
def commission_report():
    try:
        return report_service.calculate_commission()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/commission-report/download")
def download_commission_report():
    try:
        # Generate Excel → Upload to MinIO → Get presigned URL
        url = report_service.get_excel_report_and_upload()
        return JSONResponse(content={"download_url": url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/allstudents", response_model=List[StudentInput])
def list_students():
    try:
        return student.get_all_students()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/allcourses", response_model=List[CourseInput])
def list_courses():
    try:
        return course.get_all_courses()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/allenrollments", response_model=List[EnrollmentInput])
def list_enrollments():
    try:
        return enrollment.get_all_enrollments()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))