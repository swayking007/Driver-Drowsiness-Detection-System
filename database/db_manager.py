import os
import sqlite3
import hashlib
from typing import Optional, Tuple


DB_FILENAME = "save_life_users.db"


class DatabaseManager:
    """
    Simple SQLite-based user database manager.

    Handles user creation and authentication with hashed passwords.
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        """
        Initialize the database manager and ensure schema exists.

        Args:
            db_path: Optional custom path to the SQLite database file.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = db_path or os.path.join(base_dir, DB_FILENAME)

        # Ensure the directory for the database exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self._initialize_database()

    def _get_connection(self) -> sqlite3.Connection:
        """Create and return a new SQLite connection."""
        return sqlite3.connect(self.db_path)

    def _initialize_database(self) -> None:
        """Create the users table if it does not already exist."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
                conn.commit()
        except sqlite3.Error as e:
            # In a real application, this would be logged to a file
            print(f"[DB] Error initializing database: {e}")

    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Hash a password using SHA-256 with a simple static salt.

        Note:
            This is intentionally simple but avoids storing plain-text passwords.
        """
        salt = "SaveLifeStaticSalt_v1"
        return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()

    def create_user(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Create a new user with the given username and password.

        Args:
            username: Desired username (must be unique).
            password: Plain-text password (will be hashed before storage).

        Returns:
            (success, message) tuple with operation result.
        """
        username = (username or "").strip()
        if not username or not password:
            return False, "Username and password are required."

        password_hash = self._hash_password(password)

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, password_hash),
                )
                conn.commit()
            return True, "User registered successfully."
        except sqlite3.IntegrityError:
            # Username already exists
            return False, "Username already exists. Please choose another."
        except sqlite3.Error as e:
            return False, f"Database error while creating user: {e}"

    def validate_login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Validate login credentials.

        Args:
            username: Username string.
            password: Plain-text password to verify.

        Returns:
            (success, message) tuple indicating authentication result.
        """
        username = (username or "").strip()
        if not username or not password:
            return False, "Please enter both username and password."

        password_hash = self._hash_password(password)

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id FROM users WHERE username = ? AND password_hash = ?",
                    (username, password_hash),
                )
                row = cursor.fetchone()
        except sqlite3.Error as e:
            return False, f"Database error while validating login: {e}"

        if row:
            return True, "Login successful."

        return False, "Invalid username or password."

