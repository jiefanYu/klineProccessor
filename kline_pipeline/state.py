import sqlite3

class KLineStatusTracker:
    def __init__(self, db_path="kline_status.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS kline_status (
                    symbol TEXT,
                    period TEXT,
                    PRIMARY KEY (symbol, period)
                )
            """)

    def is_processed(self, symbol, period):
        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute("SELECT 1 FROM kline_status WHERE symbol=? AND period=?", (symbol, period)).fetchone()
            return result is not None

    def mark_processed(self, symbol, period):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR IGNORE INTO kline_status (symbol, period) VALUES (?, ?)", (symbol, period))
