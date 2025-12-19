# StudyRoom-Reservation-System
> 🌐 Language Switch: [Chinese](README_zh.md)

The final lab for SEU-Database_Principle.

A standalone Python desktop application based on SQLite and Tkinter, designed to implement the scenario of study room reservation on campus, with its core business functions primarily reflecting database access and manipulation operations.


## Technology stack
```
Python 3.10
 ├─ sqlite3
 ├─ Tkinter
 └─ SQL
```

## Database Design
Database: data/studyroom.db

### Student Table: `student`
Used to store basic information of students in the system, as the main body of seat reservation.

|Field Name|Type|Description|Constraint|
|---|---|---|---|
|student_id|TEXT|Student ID|Primary Key|
|name|TEXT|Student Name|Not Null|
|major|TEXT|Major|Nullable|

- `student_id` is used as the primary key to ensure student uniqueness
- One student can have multiple reservation records (1 to many)

### StudyRoom Table: `study_room`
Used to store basic information of different study rooms in the school.

|Field Name|Type|Description|Constraint|
|---|---|---|---|
|room_id|INTEGER|Study Room ID|Primary Key, Auto-increment|
|room_name|TEXT|Study Room Name|Not Null|
|location|TEXT|Study Room Location|Nullable|
|capacity|INTEGER|Seat Capacity|Nullable|

- `room_id` is the unique internal identifier of the system
- One study room can contain multiple seats

### Seat Table: `seat`
Used to store specific seat information in each study room.

|Field Name|Type|Description|Constraint|
|---|---|---|---|
|seat_id|INTEGER|Seat ID|Primary Key, Auto-increment|
|room_id|INTEGER|Belonging Study Room ID|Foreign Key|
|seat_number|INTEGER|Seat Number|Not Null|
|status|TEXT|Seat Status|Nullable|

- `room_id` foreign key references `study_room(room_id)`
- One study room corresponds to multiple seats (1 to many)
- `status` can be: Available / Disabled

### Reservation Table: `reservation`(core)
Used to record students' reservation information for seats.

|Field Name|Type|Description|Constraint|
|---|---|---|---|
|reservation_id|INTEGER|Reservation ID|Primary Key, Auto-increment|
|student_id|TEXT|Student ID|Foreign Key|
|seat_id|INTEGER|Seat ID|Foreign Key|
|reserve_date|TEXT|Reservation Date|Not Null|
|time_slot|TEXT|Time Slot|Not Null|

- **Association table** between students and seats
- Control time conflicts through `reserve_date + time_slot`
- One student can reserve multiple time slots
- One seat can only be reserved once in the same time slot (logical constraint)

## Database Create
```bash
mkdir data
python database/database.py
```

## Run
```
python main.py
```

## TODO
- ⏳ Check the validity of student ID during reservation