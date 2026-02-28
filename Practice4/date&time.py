from datetime import datetime, date, time, timedelta, timezone
from zoneinfo import ZoneInfo

now = datetime.now()
print(f"Текущая дата и время: {now}")

specific_date = datetime(2024, 12, 25, 15, 30, 45)
print(f"Конкретная дата: {specific_date}")

formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted)

date1 = datetime(2026, 1, 1)
date2 = datetime(2026, 2, 28)
difference = date2 - date1
print("Дни:", difference.days)

almaty_time = datetime.now(ZoneInfo("Asia/Almaty"))
print(almaty_time)

a = datetime.now(timezone.utc)
print(a)