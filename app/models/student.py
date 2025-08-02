from app.db import get_db_connection

def add_student(name:str, email:str):
    conn=get_db_connection()
    cur=conn.cursor()

    try:
        cur.execute("""
                    INSERT INTO students (name, email)
                    VALUES (%s, %s) RETURNING id;
                    """, (name, email))
        student_id=cur.fetchone()[0]
        conn.commit()
        return{"id":student_id, "name":name, "email":email}

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()
        conn.close()