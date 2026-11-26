# load_csv.py
# 读 devices.csv，用 pandas 的 to_sql 一行写入 SQLite
# 用法：终端进入项目6仓库目录，python load_csv.py

import sqlite3
import pandas as pd

CSV_PATH = "data/devices.csv"    # 输入：模拟器生成的数据
DB_PATH = "data/device_data.db"  # 输出：SQLite 库文件
TABLE = "device_data"            # 表名（沿用 build_db.py 的）

# 1. 读 CSV（9 个字段一次进来，dtype 自动识别）
df = pd.read_csv(CSV_PATH)

# 2. 一行写入：表已存在就整体替换，不建索引，不额外存 pandas 行号
with sqlite3.connect(DB_PATH) as conn:
    df.to_sql(TABLE, conn, if_exists="replace", index=False)

# 3. 自检：读回行数 + 猫狗分布，确认和 CSV 一致
with sqlite3.connect(DB_PATH) as conn:
    check = pd.read_sql(
        f"SELECT pet_type, COUNT(*) AS n FROM {TABLE} GROUP BY pet_type", conn
    )
print(f"入库完成：{len(df)} 行")
print(check)
