import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

FIELDS = [
    "device_id",
    "pet_type",
    "timestamp",
    "food_intake",
    "water_count",
    "weight",
    "activity_level",
    "is_anomaly",
    "anomaly_type",
]

DEVICES = [
    {"device_id": "cat-001", "pet_type": "cat", "base_weight": 4.5},
    {"device_id": "cat-002", "pet_type": "cat", "base_weight": 5.2},
    {"device_id": "dog-001", "pet_type": "dog", "base_weight": 12.0},
]


def create_normal_reading(device, timestamp):
    if device["pet_type"] == "cat":
        food_intake = random.gauss(60, 8)
        water_count = int(random.gauss(8, 2))
        activity_level = int(random.gauss(55, 12))
    else:
        food_intake = random.gauss(220, 25)
        water_count = int(random.gauss(15, 3))
        activity_level = int(random.gauss(70, 12))

    return {
        "device_id": device["device_id"],
        "pet_type": device["pet_type"],
        "timestamp": timestamp.isoformat(timespec="seconds"),
        "food_intake": round(max(0, food_intake), 1),
        "water_count": max(0, water_count),
        "weight": round(random.gauss(device["base_weight"], 0.04), 2),
        "activity_level": min(100, max(0, activity_level)),
        "is_anomaly": False,
        "anomaly_type": "none",
    }


def add_anomaly(reading):
    if random.random() >= 0.03:
        return

    anomaly_type = random.choice(
        ["low_food", "low_water", "low_activity", "weight_drop"]
    )

    if anomaly_type == "low_food":
        reading["food_intake"] = round(
            reading["food_intake"] * random.uniform(0.1, 0.4), 1
        )
    elif anomaly_type == "low_water":
        reading["water_count"] = max(
            0, reading["water_count"] - random.randint(4, 7)
        )
    elif anomaly_type == "low_activity":
        reading["activity_level"] = int(reading["activity_level"] * 0.2)
    elif anomaly_type == "weight_drop":
        reading["weight"] = round(
            reading["weight"] * random.uniform(0.88, 0.94), 2
        )

    reading["is_anomaly"] = True
    reading["anomaly_type"] = anomaly_type


def generate_records(n=1200):
    records = []
    now = datetime.now().astimezone().replace(
        hour=8, minute=0, second=0, microsecond=0
    )

    for _ in range(n):
        device = random.choice(DEVICES)
        timestamp = now - timedelta(
            days=random.randint(0, 29),
            minutes=random.randint(0, 1439),
        )
        reading = create_normal_reading(device, timestamp)
        add_anomaly(reading)
        records.append(reading)

    return records


def save_csv(records, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    random.seed(42)

    records = generate_records()
    output_path = Path(__file__).resolve().parent / "data" / "devices.csv"
    save_csv(records, output_path)

    anomaly_count = sum(record["is_anomaly"] for record in records)

    print(f"已生成 {len(records)} 条记录")
    print(f"其中异常记录 {anomaly_count} 条")
    print(f"文件位置：{output_path}")

