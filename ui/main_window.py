import tkinter as tk
from tkinter import messagebox
from ui.student_ui import StudentManager
from ui.room_ui import RoomManager
from ui.reservation_ui import ReservationManager


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("自习室座位预约管理系统")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # 系统标题
        title_label = tk.Label(
            self.root,
            text="自习室座位预约管理系统",
            font=("微软雅黑", 16, "bold")
        )
        title_label.pack(pady=30)

        # 功能按钮
        btn_student = tk.Button(
            self.root,
            text="学生管理",
            width=20,
            height=2,
            command=self.open_student_manager
        )
        btn_student.pack(pady=10)

        btn_room = tk.Button(
            self.root,
            text="自习室与座位管理",
            width=20,
            height=2,
            command=self.open_room_manager
        )
        btn_room.pack(pady=10)

        btn_reservation = tk.Button(
            self.root,
            text="座位预约",
            width=20,
            height=2,
            command=self.open_reservation_manager
        )
        btn_reservation.pack(pady=10)

        btn_exit = tk.Button(
            self.root,
            text="退出系统",
            width=20,
            height=2,
            command=self.root.quit
        )
        btn_exit.pack(pady=20)

    def open_student_manager(self):
        StudentManager(self.root)

    def open_room_manager(self):
        RoomManager(self.root)

    def open_reservation_manager(self):
        ReservationManager(self.root)