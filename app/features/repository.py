import sqlite3
from app.features.models import WaterLog
from datetime import datetime

class WaterRepository:
    def __init__(self, db_path="water.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS water_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_log(self, amount: int):
        query = "INSERT INTO water_logs (amount, timestamp) VALUES (?, ?)"
        self.conn.execute(query, (amount, datetime.now().isoformat()))
        self.conn.commit()

    def get_today_logs(self):
        today = datetime.now().date().isoformat()
        query = "SELECT id, amount, timestamp FROM water_logs"
        cursor = self.conn.execute(query)
        rows = cursor.fetchall()
        return [WaterLog(id=row[0], amount=row[1], timestamp=datetime.fromisoformat(row[2])) for row in rows if datetime.fromisoformat(row[2]).date().isoformat() == today]

    def get_total_today(self):
        logs = self.get_today_logs()
        return sum(log.amount for log in logs)