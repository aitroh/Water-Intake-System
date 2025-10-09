# database.py
"""
SQLite wrapper for Water Intake Tracker.
Manages settings and intake logs.
"""

import sqlite3
from datetime import date, datetime
from typing import List, Tuple, Optional

DB_FILE = "water_intake.db"


class Database:
    def __init__(self, db_path: str = DB_FILE):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        c = self.conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS intake (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                amount_ml INTEGER NOT NULL
            )
            """
        )
        self.conn.commit()

    # Settings (simple key/value)
    def set_setting(self, key: str, value: str):
        c = self.conn.cursor()
        c.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value)
        )
        self.conn.commit()

    def get_setting(self, key: str) -> Optional[str]:
        c = self.conn.cursor()
        c.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = c.fetchone()
        return row["value"] if row else None

    # Target helpers
    def set_daily_target_ml(self, ml: int):
        self.set_setting("daily_target_ml", str(int(ml)))

    def get_daily_target_ml(self) -> int:
        val = self.get_setting("daily_target_ml")
        if val:
            try:
                return int(val)
            except ValueError:
                return 2000
        return 2000  # default 2000 ml

    # Reminder settings
    def set_reminder_enabled(self, enabled: bool):
        self.set_setting("reminder_enabled", "1" if enabled else "0")

    def get_reminder_enabled(self) -> bool:
        val = self.get_setting("reminder_enabled")
        return val == "1"

    def set_reminder_minutes(self, minutes: int):
        self.set_setting("reminder_minutes", str(int(minutes)))

    def get_reminder_minutes(self) -> int:
        val = self.get_setting("reminder_minutes")
        if val:
            try:
                return int(val)
            except ValueError:
                return 60
        return 60

    # Intake logging
    def log_intake(self, amount_ml: int, ts: Optional[datetime] = None):
        if ts is None:
            ts = datetime.now()
        date_str = ts.date().isoformat()
        timestamp_str = ts.isoformat()
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO intake (date, timestamp, amount_ml) VALUES (?,?,?)",
            (date_str, timestamp_str, int(amount_ml)),
        )
        self.conn.commit()
        return c.lastrowid

    def update_entry_amount(self, entry_id: int, amount_ml: int):
        c = self.conn.cursor()
        c.execute(
            "UPDATE intake SET amount_ml = ? WHERE id = ?", (int(amount_ml), int(entry_id))
        )
        self.conn.commit()

    def update_entry_timestamp(self, entry_id: int, timestamp_iso: str):
        c = self.conn.cursor()
        # also update date column to match new timestamp's date
        try:
            dt = datetime.fromisoformat(timestamp_iso)
            date_str = dt.date().isoformat()
        except Exception:
            date_str = timestamp_iso.split("T")[0] if "T" in timestamp_iso else timestamp_iso
        c.execute(
            "UPDATE intake SET timestamp = ?, date = ? WHERE id = ?",
            (timestamp_iso, date_str, int(entry_id))
        )
        self.conn.commit()

    def get_intake_for_date(self, dt: str) -> int:
        """
        dt: date string 'YYYY-MM-DD'
        returns total ml for that date
        """
        c = self.conn.cursor()
        c.execute(
            "SELECT SUM(amount_ml) as total FROM intake WHERE date = ?", (dt,)
        )
        row = c.fetchone()
        return int(row["total"]) if row and row["total"] is not None else 0

    def get_entries_for_date(self, dt: str) -> List[sqlite3.Row]:
        c = self.conn.cursor()
        c.execute(
            "SELECT id, date, timestamp, amount_ml FROM intake WHERE date = ? ORDER BY timestamp ASC",
            (dt,),
        )
        return c.fetchall()

    def get_entry_by_id(self, entry_id: int) -> Optional[sqlite3.Row]:
        c = self.conn.cursor()
        c.execute("SELECT id, date, timestamp, amount_ml FROM intake WHERE id = ?", (entry_id,))
        return c.fetchone()

    def delete_entry(self, entry_id: int):
        c = self.conn.cursor()
        c.execute("DELETE FROM intake WHERE id = ?", (int(entry_id),))
        self.conn.commit()

    def get_history(self, limit: int = 14) -> List[Tuple[str, int]]:
        """
        Returns list of tuples (date_str, total_ml) ordered DESC by date.
        """
        c = self.conn.cursor()
        c.execute(
            """
            SELECT date, SUM(amount_ml) as total
            FROM intake
            GROUP BY date
            ORDER BY date DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = c.fetchall()
        return [(r["date"], int(r["total"] or 0)) for r in rows]

    def clear_entries_for_date(self, date_str):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM intake WHERE DATE(timestamp) = ?", (date_str,))
        self.conn.commit()

    def export_history_txt(self, file_path: str):
        try:
            rows = self.get_history(3650)  # get up to 10 years of data
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("Water Intake History\n")
                f.write("=====================\n\n")
                for dt, total in rows:
                    f.write(f"{dt}: {total} ml\n")
            return True  # success
        except Exception as e:
            print(f"Error exporting history: {e}")
            return False

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    # Quick smoke test
    db = Database()
    db.set_daily_target_ml(1800)
    db.log_intake(250)
    today = date.today().isoformat()
    print("Target:", db.get_daily_target_ml())
    print("Today total:", db.get_intake_for_date(today))
    print("History:", db.get_history(5))
    db.close()
