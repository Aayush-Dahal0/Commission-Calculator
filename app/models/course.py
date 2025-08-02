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