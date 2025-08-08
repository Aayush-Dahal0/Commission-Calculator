import openpyxl
from openpyxl.styles import Font
from typing import List
from app.schema.report import CommissionReport

def generate_commission_excel(data: List[CommissionReport], file_path: str) -> str:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Commission Report"

    headers = [
        "Enrollment ID", "Student ID", "Student Name", "Course ID", "Course Name",
        "Enrolled At", "Refunded?", "Refund Date", "Commission Rate",
        "Commission Amount", "Commission Type"
    ]

    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for row in data:
        ws.append([
            row.enrollment_id,
            row.student_id,
            row.student_name,
            row.course_id,
            row.course_name,
            row.enrolled_at.strftime("%Y-%m-%d"),
            "Yes" if row.is_refunded else "No",
            row.refund_date.strftime("%Y-%m-%d") if row.refund_date else "",
            f"{row.commission_rate * 100:.0f}%",
            f"NPR {row.commission_amount}",
            row.commission_type
        ])

    wb.save(file_path)
    return file_path
