import sqlite3 as sql
import os


class DBManager:
    def __init__(self):
        self.dbPath = os.path.join(os.getcwd(), "database", "data_source.db")
        self._create_messages_table()  # ✅ Ensure chat table exists on startup

    def listExtension(self):
        con = sql.connect(self.dbPath)
        cur = con.cursor()
        data = cur.execute("SELECT * FROM extension").fetchall()
        con.close()
        return data

    def get_user_by_first_name(self, first_name):
        con = sql.connect(self.dbPath)
        cur = con.cursor()
        query = "SELECT first_name, password FROM users WHERE first_name=?"
        cur.execute(query, (first_name,))
        row = cur.fetchone()
        con.close()
        if row:
            return {"first_name": row[0], "password": row[1]}
        return None

    # ======================
    # 🟩 CHAT SYSTEM METHODS
    # ======================

    def _create_messages_table(self):
        """Creates a messages table if it doesn't exist."""
        con = sql.connect(self.dbPath)
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                text TEXT NOT NULL,
                time TEXT NOT NULL
            )
            """
        )
        con.commit()
        con.close()

    def add_message(self, sender, text, time):
        """Add a new message to the chat table."""
        con = sql.connect(self.dbPath)
        cur = con.cursor()
        cur.execute(
            "INSERT INTO messages (sender, text, time) VALUES (?, ?, ?)",
            (sender, text, time),
        )
        con.commit()
        con.close()

    def get_messages(self):
        """Fetch all messages."""
        con = sql.connect(self.dbPath)
        cur = con.cursor()
        cur.execute("SELECT sender, text, time FROM messages ORDER BY id ASC")
        rows = cur.fetchall()
        con.close()
        return rows
