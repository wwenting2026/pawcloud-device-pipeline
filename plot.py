import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB = "data/device_data.db"

df = pd.read_sql("SELECT * FROM device_data", sqlite3.connect(DB))
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

normal = df[df["is_anomaly"] == 0]
anomaly = df[df["is_anomaly"] == 1]

metrics = [("food_intake", "Food intake (g)"),
           ("water_count", "Water count"),
           ("activity_level", "Activity level")]

fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)

for ax, (col, label) in zip(axes, metrics):
    ax.scatter(normal["timestamp"], normal[col], c="green", s=8, alpha=0.5, label="normal")
    ax.scatter(anomaly["timestamp"], anomaly[col], c="red", s=25, label="anomaly")
    ax.set_ylabel(label)
    ax.legend(loc="upper right")

axes[-1].set_xlabel("Time")
plt.tight_layout()
plt.savefig("data/visualization.png", dpi=150)
plt.show()
print("图已保存：data/visualization.png")