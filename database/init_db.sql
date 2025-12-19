-- 学生表
CREATE TABLE IF NOT EXISTS student (
    student_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    major TEXT
);

-- 自习室表
CREATE TABLE IF NOT EXISTS study_room (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name TEXT NOT NULL,
    location TEXT,
    capacity INTEGER
);

-- 座位表
CREATE TABLE IF NOT EXISTS seat (
    seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    seat_number INTEGER NOT NULL,
    status TEXT,
    FOREIGN KEY (room_id) REFERENCES study_room(room_id)
);

-- 预约表
CREATE TABLE IF NOT EXISTS reservation (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    seat_id INTEGER NOT NULL,
    reserve_date TEXT NOT NULL,
    time_slot TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (seat_id) REFERENCES seat(seat_id)
);
