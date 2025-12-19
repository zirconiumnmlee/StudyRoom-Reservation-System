import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from dao.reservation_dao import (
    get_available_seats,
    reserve_seat,
    get_reservations_by_student
)

# 参数准备
room_id = 1
student_id = "20230001"
date = "2025-01-01"
time_slot = "08:00-10:00"

# 查询可用座位
seats = get_available_seats(room_id, date, time_slot)
print("Available seats:", seats)

# 预约第一个可用座位
if seats:
    seat_id = seats[0][0]
    success = reserve_seat(student_id, seat_id, date, time_slot)
    print("Reserve result:", success)

# 查询学生预约记录
records = get_reservations_by_student(student_id)
print("Reservation records:")
for r in records:
    print(r)
