import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from dao.room_dao import get_all_study_rooms
from dao.reservation_dao import (
    get_available_seats,
    add_reservation,
    get_all_reservations
)


class ReservationManager:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("座位预约管理")
        self.window.geometry("800x480")
        self.window.resizable(False, False)

        self.rooms = []
        self.seats = []

        # ✅ 关键三行
        self.window.transient(parent)   # 依附于主窗口
        self.window.grab_set()           # 抢占所有事件（主窗口不能点）
        self.window.focus_set()          # 焦点在子窗口

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

        self.create_widgets()
        self.load_rooms()
        self.load_reservations()
    
    def on_close(self):
        self.window.grab_release()
        self.window.destroy()


    def create_widgets(self):
        # ===== 输入区 =====
        frame_input = tk.Frame(self.window)
        frame_input.pack(pady=10)

        tk.Label(frame_input, text="学号：").grid(row=0, column=0)
        self.entry_student = tk.Entry(frame_input, width=12)
        self.entry_student.grid(row=0, column=1, padx=5)

        tk.Label(frame_input, text="预约日期(YYYY-MM-DD)：").grid(row=0, column=2)
        self.entry_date = tk.Entry(frame_input, width=14)
        self.entry_date.grid(row=0, column=3, padx=5)

        tk.Label(frame_input, text="时间段：").grid(row=1, column=0)
        self.combo_time = ttk.Combobox(
            frame_input,
            state="readonly",
            values=["08:00-10:00", "10:00-12:00", "14:00-16:00", "16:00-18:00"],
            width=14
        )
        self.combo_time.grid(row=1, column=1, padx=5)

        tk.Label(frame_input, text="自习室：").grid(row=0, column=4)
        self.combo_room = ttk.Combobox(frame_input, state="readonly", width=16)
        self.combo_room.grid(row=0, column=5, padx=5)

        tk.Button(
            frame_input, text="查询可用座位", command=self.load_seats
        ).grid(row=0, column=6, padx=5)

        # ===== 座位选择 =====
        frame_seat = tk.Frame(self.window)
        frame_seat.pack(pady=5)

        tk.Label(frame_seat, text="可用座位：").pack(side=tk.LEFT)
        self.combo_seat = ttk.Combobox(frame_seat, state="readonly", width=20)
        self.combo_seat.pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame_seat, text="预约座位", command=self.make_reservation
        ).pack(side=tk.LEFT, padx=10)

        # ===== 预约记录表 =====
        frame_table = tk.Frame(self.window)
        frame_table.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ("id", "student_id", "name", "room", "seat", "date", "time_slot")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")

        headers = ["ID", "学号", "姓名", "自习室", "座位号", "日期", "时间段"]
        column_widths = [50, 90, 80, 120, 70, 90, 100]

        for col, header, width in zip(columns, headers, column_widths):
            self.tree.heading(col, text=header)
            self.tree.column(col, width=width, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_rooms(self):
        self.rooms = get_all_study_rooms()
        room_names = [f"{r[0]} - {r[1]}" for r in self.rooms]
        self.combo_room["values"] = room_names

    def load_seats(self):
        if not self.combo_room.get() or not self.entry_date.get():
            messagebox.showwarning("提示", "请选择自习室并输入日期", parent=self.window)
            return
        if not self.combo_time.get():
            messagebox.showwarning("提示", "请选择时间段", parent=self.window)
        time_slot = self.combo_time.get()
        room_id = int(self.combo_room.get().split(" - ")[0])
        date = self.entry_date.get().strip()

        self.seats = get_available_seats(room_id, date, time_slot)
        seat_values = [f"{s[0]} - 座位{s[1]}" for s in self.seats]
        self.combo_seat["values"] = seat_values

    def make_reservation(self):
        student_id = self.entry_student.get().strip()
        date = self.entry_date.get().strip()
        time_slot = self.combo_time.get()

        if not time_slot:
            messagebox.showwarning("提示", "请选择时间段", parent=self.window)
            return

        if not student_id or not self.combo_seat.get():
            messagebox.showwarning("提示", "信息不完整", parent=self.window)
            return

        seat_id = int(self.combo_seat.get().split(" - ")[0])

        try:
            add_reservation(student_id, seat_id, date, time_slot)
            messagebox.showinfo("成功", "预约成功", parent=self.window)
            self.load_reservations()
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "错误",
                "学号不存在，请先添加学生",
                parent=self.window
            )
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.window)

    def load_reservations(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = get_all_reservations()
        for r in records:
            self.tree.insert("", tk.END, values=r)
