import tkinter as tk
from ui.main_window import MainWindow
from database.database import init_database


def main():
    init_database()

    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
