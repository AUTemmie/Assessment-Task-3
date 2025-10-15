import sqlite3 as sql
import os


class DBManager:
    def __init__(self):
        # Ensure database folder exists
        db_dir = os.path.join(os.getcwd(), "database")
        os.makedirs(db_dir, exist_ok=True)

        # Define database path
        self.dbPath = os.path.join(db_dir, "data_source.db")

        # Ensure tables exist
        self._create_messages_table()
        self._create_users_table()
        self._create_extension_table()

    def listExtension(self):
        """Return all rows from the extension table."""
        con = sql.connect(self.dbPath)
        cur = con.cursor()
        cur.execute("SELECT * FROM extension")
        data = cur.fetchall()
        con.close()
        return data

    def get_user_by_first_name(self, first_name):
        """Return user data by first name."""
        con = sql.connect(self.dbPath)
        cur = con.cursor()
        query = "SELECT first_name, password FROM users WHERE first_name = ?"
        cur.execute(query, (first_name,))
        row = cur.fetchone()
        con.close()
        if row:
            return {"first_name": row[0], "password": row[1]}
        return None

    # CHAT SYSTEM
    def _create_messages_table(self):
        """Create messages table if it doesn't exist."""
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

    # EXTRA TABLES FOR STABILITY
    def _create_users_table(self):
        """Create users table if it doesn't exist."""
        con = sql.connect(self.dbPath)
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                password TEXT NOT NULL
            )
            """
        )
        con.commit()
        con.close()

    def _create_extension_table(self):
        """Create extension table if it doesn't exist."""
        con = sql.connect(self.dbPath)
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS extension (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                version TEXT
            )
            """
        )
        con.commit()
        con.close()
