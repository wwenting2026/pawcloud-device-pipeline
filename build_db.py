# build_db.py — 项目6：读取 CSV，建 SQLite 库（device_data 表）
# 用法：把本文件放在仓库根目录（和 simulator.py 同级），运行  python build_db.py
import sqlite3
import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent                 # 仓库根目录
CSV_PATH = BASE / "data" / "devices.csv"
DB_PATH = BASE / "data" / "device_data.db"

# 表结构定稿：字段和 CSV 完全一致
CREATE_SQL = """
CREATE TABLE IF NOT EXISTS device_data (
    device_id      TEXT,      -- 设备号，如 DEV-2132
    pet_type       TEXT,      -- cat / dog
    timestamp      TEXT,      -- ISO 格式，文本即可排序
    food_intake    REAL,      -- 食量
    water_count    INTEGER,   -- 饮水次数
    weight         REAL,      -- 体重
    activity_level REAL,      -- 活动量
    is_anomaly     INTEGER,   -- 0=正常 1=异常
    anomaly_type   TEXT       -- none / blocked_food / water_drop / activity_drop
);
"""

def main():
    df = pd.read_csv(CSV_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(CREATE_SQL)                  # 1. 建表（已存在则跳过）
    cur.execute("DELETE FROM device_data")   # 2. 清空旧数据，保证可重复运行
    cur.executemany(                         # 3. 批量插入
        "INSERT INTO device_data VALUES (?,?,?,?,?,?,?,?,?)",
        df.itertuples(index=False, name=None),
    )
    conn.commit()

    # 自检：行数 + 猫狗分布
    n = cur.execute("SELECT COUNT(*) FROM device_data").fetchone()[0]
    pets = cur.execute("SELECT pet_type, COUNT(*) FROM device_data GROUP BY pet_type").fetchall()
    print(f"OK 建库完成：{DB_PATH}")
    print(f"   共 {n} 行，CSV 也是 {len(df)} 行 -> 数量{'一致' if n == len(df) else '不一致！'}")
    print(f"   猫狗分布：{pets}")
    conn.close()

if __name__ == "__main__":
    main()
