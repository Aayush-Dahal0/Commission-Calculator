from app.db import get_db_connection

def add_course(name,course_type,base_price):
    conn=get_db_connection()
    cur=conn.cursor()

    try:
        cur.execute("""
        INSERT INTO courses(name,course_type,base_price)
                    VALUES(%s,%s,%s) RETURNING id;
                    """,(name,course_type,base_price))
        course_id=cur.fetchone()[0]
        conn.commit()
        return{"id":course_id,
               "name":name,
               "course_type":course_type,
               "base_price":base_price}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def get_all_courses():
    conn=get_db_connection()
    cur=conn.cursor()
    try:
        cur.execute("SELECT id, name, course_type, base_price FROM courses;")
        rows=cur.fetchall()
        courses=[{"id": row[0], "name": row[1], "course_type": row[2], "base_price": row[3]} for row in rows]
        return courses
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()