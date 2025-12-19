from database.database import get_connection


def add_student(student_id, name, major):
    """
    添加学生信息
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO student (student_id, name, major)
    VALUES (?, ?, ?)
    """
    try:
        cursor.execute(sql, (student_id, name, major))
        conn.commit()
    except Exception as e:
        print("Add student failed:", e)
    finally:
        conn.close()


def get_all_students():
    """
    查询所有学生
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = "SELECT student_id, name, major FROM student"
    cursor.execute(sql)
    rows = cursor.fetchall()

    conn.close()
    return rows


def delete_student(student_id):
    """
    删除学生
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = "DELETE FROM student WHERE student_id = ?"
    cursor.execute(sql, (student_id,))
    conn.commit()

    conn.close()
