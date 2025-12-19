import sqlite3
import os

# 数据库文件路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "studyroom.db")

def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_database():
    """初始化数据库（建表）"""
    conn = get_connection()
    cursor = conn.cursor()

    sql_file = os.path.join(os.path.dirname(__file__), "init_db.sql")
    with open(sql_file, "r", encoding="utf-8") as f:
        sql_script = f.read()

    cursor.executescript(sql_script)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_database()
