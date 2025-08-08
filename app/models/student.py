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

def get_all_students():
    conn=get_db_connection()
    cur=conn.cursor()
    try:
        cur.execute("SELECT id, name, email FROM students;")
        rows=cur.fetchall()
        students=[{"id": row[0], "name": row[1], "email": row[2]} for row in rows]
        return students
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
   

    