from database.database import get_connection


def get_available_seats(room_id, reserve_date, time_slot):
    """
    查询某天某时间段某自习室中未被预约的座位
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    SELECT s.seat_id, s.seat_number
    FROM seat s
    WHERE s.room_id = ?
      AND s.seat_id NOT IN (
          SELECT seat_id
          FROM reservation
          WHERE reserve_date = ?
            AND time_slot = ?
      )
    ORDER BY s.seat_number
    """

    cursor.execute(sql, (room_id, reserve_date, time_slot))
    seats = cursor.fetchall()
    conn.close()
    return seats



def add_reservation(student_id, seat_id, reserve_date, time_slot):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO reservation (student_id, seat_id, reserve_date, time_slot)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(sql, (student_id, seat_id, reserve_date, time_slot))
    conn.commit()
    conn.close()



def get_all_reservations():
    """
    查询所有预约记录（多表连接，包含时间段）
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    SELECT
        r.reservation_id,
        st.student_id,
        st.name,
        sr.room_name,
        s.seat_number,
        r.reserve_date,
        r.time_slot
    FROM reservation r
    JOIN student st ON r.student_id = st.student_id
    JOIN seat s ON r.seat_id = s.seat_id
    JOIN study_room sr ON s.room_id = sr.room_id
    ORDER BY r.reserve_date, r.time_slot
    """

    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows

