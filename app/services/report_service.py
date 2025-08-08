from decimal import Decimal
from app.db import get_db_connection
from app.schema.report import CommissionReport
from app.utils.excel_utils import generate_commission_excel
from app.utils.minio_utils import upload_file_to_minio, get_presigned_url

from tempfile import gettempdir
from datetime import datetime
import os

def calculate_commission():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 
                e.id as enrollment_id,
                s.id as student_id,
                s.name as student_name,
                c.id as course_id,
                c.name as course_name,
                c.base_price as base_price,
                e.enrolled_at,
                e.is_refunded,
                e.refund_date
            FROM enrollments e
            JOIN students s ON e.student_id = s.id
            JOIN courses c ON e.course_id = c.id
        """)

        rows = cur.fetchall()
        results = []

        for row in rows:
            enrollment_id, student_id, student_name, course_id, course_name, base_price, enrolled_at, is_refunded, refund_date = row
            base_price = Decimal(str(base_price))

            if is_refunded:
                commission_rate = Decimal("0.00")
                commission_type = "Refunded"
            elif enrolled_at.day <= 15:
                commission_rate = Decimal("0.20")
                commission_type = "Early"
            else:
                commission_rate = Decimal("0.10")
                commission_type = "Late"

            commission_amount = base_price * commission_rate

            results.append({
                "enrollment_id": enrollment_id,
                "student_id": student_id,
                "student_name": student_name,
                "course_id": course_id,
                "course_name": course_name,
                "enrolled_at": enrolled_at,
                "is_refunded": is_refunded,
                "refund_date": refund_date,
                "commission_rate": float(commission_rate),
                "commission_amount": float(commission_amount),
                "commission_type": commission_type,
            })

        return results

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def get_excel_report_and_upload():
    raw_data = calculate_commission()
    data = [CommissionReport(**item) for item in raw_data]

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"commission_report_{timestamp}.xlsx"
    file_path = os.path.join(gettempdir(), filename)

    generate_commission_excel(data, file_path)

    # Upload to MinIO and get file key
    key = f"reports/{filename}"
    upload_file_to_minio(file_path, key)

    # Get presigned URL
    url = get_presigned_url(key)
    return url
