from pydantic import BaseModel
from typing import Optional
from datetime import date

class CommissionReport(BaseModel):
    enrollment_id: int
    student_id: int
    student_name: str
    course_id: int
    course_name: str
    enrolled_at: date
    is_refunded: bool
    refund_date: Optional[date]
    commission_rate: float
    commission_amount: float
    commission_type: str
