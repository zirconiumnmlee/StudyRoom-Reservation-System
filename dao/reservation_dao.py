from database.database import get_connection


def get_available_seats(room_id, reserve_date, time_slot):
    """
    查询某自习室在指定日期和时间段的可用座位
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    SELECT s.seat_id, s.seat_number
    FROM seat s
    WHERE s.room_id = ?
    AND s.seat_id NOT IN (
        SELECT r.seat_id
        FROM reservation r
        WHERE r.reserve_date = ?
        AND r.time_slot = ?
    )
    ORDER BY s.seat_number
    """

    cursor.execute(sql, (room_id, reserve_date, time_slot))
    seats = cursor.fetchall()

    conn.close()
    return seats


def reserve_seat(student_id, seat_id, reserve_date, time_slot):
    """
    预约座位（带冲突检测）
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 先检查该座位是否已被预约
    check_sql = """
    SELECT COUNT(*)
    FROM reservation
    WHERE seat_id = ?
    AND reserve_date = ?
    AND time_slot = ?
    """
    cursor.execute(check_sql, (seat_id, reserve_date, time_slot))
    count = cursor.fetchone()[0]

    if count > 0:
        conn.close()
        return False  # 预约失败，座位已被占用

    # 执行预约
    insert_sql = """
    INSERT INTO reservation (student_id, seat_id, reserve_date, time_slot)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(insert_sql, (student_id, seat_id, reserve_date, time_slot))
    conn.commit()

    conn.close()
    return True


def cancel_reservation(reservation_id):
    """
    取消预约
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = "DELETE FROM reservation WHERE reservation_id = ?"
    cursor.execute(sql, (reservation_id,))
    conn.commit()

    conn.close()


def get_reservations_by_student(student_id):
    """
    查询某学生的预约记录（多表 JOIN）
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    SELECT r.reservation_id,
           sr.room_name,
           s.seat_number,
           r.reserve_date,
           r.time_slot
    FROM reservation r
    JOIN seat s ON r.seat_id = s.seat_id
    JOIN study_room sr ON s.room_id = sr.room_id
    WHERE r.student_id = ?
    ORDER BY r.reserve_date, r.time_slot
    """

    cursor.execute(sql, (student_id,))
    records = cursor.fetchall()

    conn.close()
    return records
