from database.database import get_connection


def add_study_room(room_name, location, capacity):
    """
    添加自习室
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO study_room (room_name, location, capacity)
    VALUES (?, ?, ?)
    """
    cursor.execute(sql, (room_name, location, capacity))
    conn.commit()

    room_id = cursor.lastrowid  # 获取刚插入的自习室ID
    conn.close()
    return room_id


def get_all_study_rooms():
    """
    查询所有自习室
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = "SELECT room_id, room_name, location, capacity FROM study_room"
    cursor.execute(sql)
    rooms = cursor.fetchall()

    conn.close()
    return rooms


def init_seats_for_room(room_id, seat_count):
    """
    为指定自习室初始化座位
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO seat (room_id, seat_number)
    VALUES (?, ?)
    """

    for i in range(1, seat_count + 1):
        cursor.execute(sql, (room_id, i))

    conn.commit()
    conn.close()


def get_seats_by_room(room_id):
    """
    查询某个自习室的所有座位
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    SELECT seat_id, seat_number
    FROM seat
    WHERE room_id = ?
    ORDER BY seat_number
    """
    cursor.execute(sql, (room_id,))
    seats = cursor.fetchall()

    conn.close()
    return seats
