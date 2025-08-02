from app.db import get_db_connection
from datetime import date
def add_enrollment(student_id,course_id,enrolled_at,is_refunded,refund_date):
    conn=get_db_connection()
    cur=conn.cursor()

    try:
        cur.execute("""
        INSERT INTO enrollments(student_id,course_id,enrolled_at,is_refunded,refund_date)
        VALUES(%s,%s,COALESCE(%s, CURRENT_DATE),%s,%s) RETURNING id;
        """,(student_id,course_id,enrolled_at,is_refunded,refund_date))
        enrolled_at=cur.fetchone()[0]
        conn.commit()
        return{
            "student_id":student_id,
            "course_id":course_id,
            "enrolled_at":enrolled_at if enrolled_at else date.today(),
            "is_refunded":is_refunded,
            "refund_date":refund_date
        }
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()