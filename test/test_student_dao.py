import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from dao.student_dao import add_student, get_all_students, delete_student

# 添加学生
add_student("20230001", "张三", "计算机科学与技术")
add_student("20230002", "李四", "软件工程")

# 查询学生
students = get_all_students()
print("All students:")
for s in students:
    print(s)

# 删除学生
delete_student("20230002")

print("After delete:")
students = get_all_students()
for s in students:
    print(s)
