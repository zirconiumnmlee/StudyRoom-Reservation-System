# StudyRoom-Reservation-System
> 🌐 语言切换：[English](README.md)

东南大学《数据库原理》课程期末实验项目。

基于 SQLite 和 Tkinter 开发的 Python 单机桌面应用，实现校园自习室预约场景，核心业务功能聚焦数据库的访问与操作。

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

用于存储系统中学生的基本信息，作为座位预约的主体。


|字段名|类型|说明|约束|
|---|---|---|---|
|student_id|TEXT|学号|主键|
|name|TEXT|学生姓名|非空|
|major|TEXT|专业|可空|


- 使用 `student_id` 作为主键，保证学生唯一性
- 一个学生可以有多条预约记录（1 对多）
    

### StudyRoom Table: `study_room`

用于存储学校内不同自习室的基本信息。

|字段名|类型|说明|约束|
|---|---|---|---|
|room_id|INTEGER|自习室编号|主键，自增|
|room_name|TEXT|自习室名称|非空|
|location|TEXT|自习室位置|可空|
|capacity|INTEGER|座位容量|可空|

- `room_id` 为系统内部唯一标识
- 一个自习室可以包含多个座位


### Seat Table: `seat`

用于存储每个自习室中的具体座位信息。

|字段名|类型|说明|约束|
|---|---|---|---|
|seat_id|INTEGER|座位编号|主键，自增|
|room_id|INTEGER|所属自习室编号|外键|
|seat_number|INTEGER|座位号|非空|
|status|TEXT|座位状态|可空|

- `room_id` 外键引用 `study_room(room_id)`
- 一个自习室对应多个座位（1 对多）
- `status` 可表示：可用 / 停用

### Reservation Table: `reservation`(core)

用于记录学生对座位的预约信息。

|字段名|类型|说明|约束|
|---|---|---|---|
|reservation_id|INTEGER|预约编号|主键，自增|
|student_id|TEXT|学号|外键|
|seat_id|INTEGER|座位编号|外键|
|reserve_date|TEXT|预约日期|非空|
|time_slot|TEXT|时间段|非空|

- 学生与座位的**关联表**
- 通过 `reserve_date + time_slot` 控制时间冲突
- 一个学生可预约多个时间段
- 一个座位在同一时间段只能被预约一次（逻辑约束）

## Database Create
```
mkdir data
python database/database.py
```

## Run
```
python main.py
```

## TODO
- ⏳ 预约时检查学号是否合法
- ⏳ E-R图