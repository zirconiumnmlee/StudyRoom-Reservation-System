import tkinter as tk
from tkinter import ttk, messagebox

from dao.room_dao import (
    add_study_room,
    get_all_study_rooms,
    init_seats_for_room
)


class RoomManager:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("自习室与座位管理")
        self.window.geometry("700x420")
        self.window.resizable(False, False)

        self.create_widgets()
        self.load_rooms()

    def create_widgets(self):
        # ===== 输入区 =====
        frame_input = tk.Frame(self.window)
        frame_input.pack(pady=10)

        tk.Label(frame_input, text="自习室名称：").grid(row=0, column=0, padx=5)
        self.entry_name = tk.Entry(frame_input, width=15)
        self.entry_name.grid(row=0, column=1, padx=5)

        tk.Label(frame_input, text="位置：").grid(row=0, column=2, padx=5)
        self.entry_location = tk.Entry(frame_input, width=15)
        self.entry_location.grid(row=0, column=3, padx=5)

        tk.Label(frame_input, text="容量(座位数)：").grid(row=0, column=4, padx=5)
        self.entry_capacity = tk.Entry(frame_input, width=10)
        self.entry_capacity.grid(row=0, column=5, padx=5)

        # ===== 按钮区 =====
        frame_btn = tk.Frame(self.window)
        frame_btn.pack(pady=10)

        tk.Button(
            frame_btn, text="添加自习室", width=14, command=self.add_room
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            frame_btn, text="刷新列表", width=14, command=self.load_rooms
        ).grid(row=0, column=1, padx=10)

        # ===== 表格区 =====
        frame_table = tk.Frame(self.window)
        frame_table.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ("room_id", "room_name", "location", "capacity")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")

        self.tree.heading("room_id", text="ID")
        self.tree.heading("room_name", text="自习室名称")
        self.tree.heading("location", text="位置")
        self.tree.heading("capacity", text="容量")

        self.tree.column("room_id", width=60, anchor=tk.CENTER)
        self.tree.column("room_name", width=180, anchor=tk.CENTER)
        self.tree.column("location", width=180, anchor=tk.CENTER)
        self.tree.column("capacity", width=100, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_rooms(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        rooms = get_all_study_rooms()
        for r in rooms:
            self.tree.insert("", tk.END, values=r)

    def add_room(self):
        name = self.entry_name.get().strip()
        location = self.entry_location.get().strip()
        capacity = self.entry_capacity.get().strip()

        if not name or not location or not capacity:
            messagebox.showwarning("提示", "请填写完整信息", parent=self.window)
            return

        if not capacity.isdigit():
            messagebox.showwarning("提示", "容量必须是数字", parent=self.window)
            return

        capacity = int(capacity)

        try:
            # 1️⃣ 添加自习室
            room_id = add_study_room(name, location, capacity)

            # 2️⃣ 初始化座位
            init_seats_for_room(room_id, capacity)

            messagebox.showinfo("成功", "自习室及座位初始化完成", parent=self.window)
            self.load_rooms()
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.window)
