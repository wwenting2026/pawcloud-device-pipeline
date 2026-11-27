# PawCloud 设备数据管道（FDE 交付一 · 进行中）

虚构客户"派云 PawCloud"（宠物智能硬件公司）：设备上云后数据有了，但没人看得出问题。本项目搭建从数据仿真 → 清洗 → 异常检测的设备数据底座。

## 当前进度：数据仿真与自检（第 1 阶段）

- `simulator.py`：Python 模拟器，生成猫/狗双物种传感器数据 1200 条，两套基线 + 传感器噪声
- 人工注入 3 类异常：堵粮（blocked_food）、饮水骤降（low_water）、活动骤降（low_activity），约 3%
- `data/devices.csv`：仿真输出（9 字段：device_id / pet_type / timestamp / food_intake / water_count / weight / activity_level / is_anomaly / anomaly_type）
- 数据自检（见 notebook）：
  - 总体 describe() 分布正常，无离谱值
  - 分组均值验证：猫狗基线显著不同（food_intake 猫 59.6 vs 狗 217.3，weight 4.86 vs 11.99）
  - 异常行特征复核 + 随机抽 20 行人工核对，标记无误

## 运行方法

```bash
python simulator.py   # 重新生成 data/devices.csv
jupyter lab           # 打开数据自检 notebook
'''

## 数据库说明
- 数据库：SQLite（data/device_data.db）
- 表：device_data（device_id / pet_type / timestamp / food_intake / is_anomaly）
- 复现顺序：python build_db.py → 用 queries.sql 验证
- 预期结果：总条数 1200，异常 31 条
