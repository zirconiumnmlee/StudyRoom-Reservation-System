import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from dao.room_dao import (
    add_study_room,
    get_all_study_rooms,
    init_seats_for_room,
    get_seats_by_room
)

# 添加自习室
room_id = add_study_room("第一自习室", "教学楼A", 10)
print("New room id:", room_id)

# 初始化座位
init_seats_for_room(room_id, 10)

# 查询自习室
rooms = get_all_study_rooms()
print("Study rooms:")
for r in rooms:
    print(r)

# 查询座位
seats = get_seats_by_room(room_id)
print("Seats in room:")
for s in seats:
    print(s)
