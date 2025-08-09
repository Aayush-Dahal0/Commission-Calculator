from app.db import get_db_connection
from datetime import date

def add_enrollment(student_id, course_id, enrolled_at=None, is_refunded=False, refund_date=None):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Prevent duplicate enrollment
        cur.execute("""
            SELECT id FROM enrollments
            WHERE student_id = %s AND course_id = %s
        """, (student_id, course_id))
        if cur.fetchone():
            raise Exception("This student is already enrolled in the course.")

        # Default enrolled_at to today if None
        if not enrolled_at:
            enrolled_at = date.today()

        cur.execute("""
            INSERT INTO enrollments(student_id, course_id, enrolled_at, is_refunded, refund_date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (student_id, course_id, enrolled_at, is_refunded, refund_date))

        enrollment_id = cur.fetchone()[0]
        conn.commit()

        return {
            "id": enrollment_id,
            "student_id": student_id,
            "course_id": course_id,
            "enrolled_at": enrolled_at,
            "is_refunded": is_refunded,
            "refund_date": refund_date
        }

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def get_all_enrollments():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, student_id, course_id, enrolled_at, is_refunded, refund_date
            FROM enrollments;
        """)
        rows = cur.fetchall()
        return [
            {
                "id": row[0],
                "student_id": row[1],
                "course_id": row[2],
                "enrolled_at": row[3],
                "is_refunded": row[4],
                "refund_date": row[5]
            }
            for row in rows
        ]
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def get_enrollment_by_student_course(student_id, course_id):
    """Return enrollment if a student is already enrolled in a course, else None"""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, student_id, course_id, enrolled_at, is_refunded, refund_date
            FROM enrollments
            WHERE student_id = %s AND course_id = %s
        """, (student_id, course_id))
        row = cur.fetchone()
        if row:
            return {
                "id": row[0],
                "student_id": row[1],
                "course_id": row[2],
                "enrolled_at": row[3],
                "is_refunded": row[4],
                "refund_date": row[5]
            }
        return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
