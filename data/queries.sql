SELECT COUNT(*) FROM device_data;

SELECT COUNT(*) FROM device_data WHERE is_anomaly = 1;

SELECT pet_type, ROUND(AVG(food_intake), 2) FROM device_data GROUP BY pet_type;
#这个是用来验收device_date.db的
