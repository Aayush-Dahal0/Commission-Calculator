from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,EmailStr
from app.models import student,course,enrollment

from datetime import date
from dotenv import load_dotenv
load_dotenv()
app=FastAPI()

class StudentInput(BaseModel):
    name:str
    email:EmailStr

class CourseInput(BaseModel):
    name:str
    course_type:str
    base_price:float

class EnrollmentInput(BaseModel):
    student_id:int
    course_id:int
    enrolled_at:date
    is_refunded:bool
    refund_date:date

@app.post("/students")
def create_student(data:StudentInput):
    try:
        result=student.add_student(data.name,str(data.email))
        return result
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

@app.post("/courses")
def create_courses(data:CourseInput):
    try:
        result=course.add_course(data.name,data.course_type,data.base_price)
        return result
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

@app.post("/enrolled")
def create_enrollment(data:EnrollmentInput):
    try:
        result=enrollment.add_enrollment(data.student_id,data.course_id,data.enrolled_at,data.is_refunded,data.refund_date)
        return result
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
