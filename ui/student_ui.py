import tkinter as tk
from tkinter import ttk, messagebox

from dao.student_dao import add_student, get_all_students, delete_student


class StudentManager:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("学生管理")
        self.window.geometry("600x400")
        self.window.resizable(False, False)

        self.create_widgets()
        self.load_students()

    def create_widgets(self):
        # ===== 输入区域 =====
        frame_input = tk.Frame(self.window)
        frame_input.pack(pady=10)

        tk.Label(frame_input, text="学号：").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = tk.Entry(frame_input)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="姓名：").grid(row=0, column=2, padx=5, pady=5)
        self.entry_name = tk.Entry(frame_input)
        self.entry_name.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_input, text="专业：").grid(row=1, column=0, padx=5, pady=5)
        self.entry_major = tk.Entry(frame_input)
        self.entry_major.grid(row=1, column=1, padx=5, pady=5)

        # ===== 按钮区域 =====
        frame_btn = tk.Frame(self.window)
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="添加学生", width=12, command=self.add_student).grid(
            row=0, column=0, padx=10
        )
        tk.Button(frame_btn, text="删除学生", width=12, command=self.delete_student).grid(
            row=0, column=1, padx=10
        )
        tk.Button(frame_btn, text="刷新列表", width=12, command=self.load_students).grid(
            row=0, column=2, padx=10
        )

        # ===== 学生列表 =====
        frame_table = tk.Frame(self.window)
        frame_table.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ("student_id", "name", "major")
        self.tree = ttk.Treeview(
            frame_table, columns=columns, show="headings"
        )

        self.tree.heading("student_id", text="学号")
        self.tree.heading("name", text="姓名")
        self.tree.heading("major", text="专业")

        self.tree.column("student_id", width=150, anchor=tk.CENTER)
        self.tree.column("name", width=150, anchor=tk.CENTER)
        self.tree.column("major", width=200, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_students(self):
        # 清空表格
        for item in self.tree.get_children():
            self.tree.delete(item)

        students = get_all_students()
        for s in students:
            self.tree.insert("", tk.END, values=s)

    def add_student(self):
        student_id = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        major = self.entry_major.get().strip()

        if not student_id or not name:
            messagebox.showwarning("提示", "学号和姓名不能为空", parent=self.window)
            return

        try:
            add_student(student_id, name, major)
            messagebox.showinfo("成功", "学生添加成功", parent=self.window)
            self.load_students()
        except Exception as e:
            messagebox.showerror("错误", str(e), parent=self.window)

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择要删除的学生", parent=self.window)
            return

        student_id = self.tree.item(selected[0])["values"][0]
        delete_student(student_id)
        messagebox.showinfo("成功", "学生删除成功", parent=self.window)
        self.load_students()
