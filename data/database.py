"""
Rune AI — Database Module

Handles all SQLite database operations for Rune AI. This includes:
- Creating the data directory if it doesn't exist
- Creating the SQLite database file if it doesn't exist
- Initializing tables on first run
- Providing a connection helper function

The database file is stored at: data/runeai.db (relative to the project root).
All file paths are built using pathlib, so this works on any operating system.
"""

import sqlite3
from pathlib import Path


# ---------------------------------------------------------------------------
# Database path — resolved relative to the Rune AI project folder
# ---------------------------------------------------------------------------
# __file__ is this file's path (e.g. .../Rune AI/data/database.py).
# We go up one level (data/) to get the project root, then append data/runeai.db.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent  # Rune AI/
_DATA_DIR = _PROJECT_ROOT / "data"                      # Rune AI/data/
_DB_PATH = _DATA_DIR / "runeai.db"                      # Rune AI/data/runeai.db


# ---------------------------------------------------------------------------
# Table definitions — each is a CREATE TABLE statement.
# ---------------------------------------------------------------------------
# These use parameter placeholders (e.g. ?) where appropriate, though
# DDL statements don't accept parameters. The structure is kept minimal
# now and will be expanded later as we learn what fields Rune AI needs.

_CREATE_MONSTERS_TABLE = """
CREATE TABLE IF NOT EXISTS monsters (
    id              INTEGER PRIMARY KEY,
    name            TEXT    UNIQUE NOT NULL,
    combat_level    INTEGER,
    hitpoints       INTEGER,
    attack_level    INTEGER,
    strength_level  INTEGER,
    defence_level   INTEGER,
    magic_level     INTEGER,
    ranged_level    INTEGER,
    location        TEXT,
    wiki_url        TEXT
);
"""

_CREATE_ITEMS_TABLE = """
CREATE TABLE IF NOT EXISTS items (
    id      INTEGER PRIMARY KEY,
    name    TEXT    UNIQUE NOT NULL,
    examine TEXT,
    wiki_url TEXT
);
"""

_CREATE_LOCATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS locations (
    id          INTEGER PRIMARY KEY,
    name        TEXT    UNIQUE NOT NULL,
    description TEXT,
    wiki_url    TEXT
);
"""


# ---------------------------------------------------------------------------
# Initialization and connection helpers
# ---------------------------------------------------------------------------

def init_database() -> None:
    """Initialize the Rune AI database.

    This function does three things:
      1. Creates the `data/` directory if it doesn't already exist.
      2. Opens (or creates) the SQLite database file at data/runeai.db.
      3. Runs CREATE TABLE statements for all known tables.

    Tables are only created once — if they already exist, SQLite silently
    skips them thanks to the `IF NOT EXISTS` clause. This means you can
    call init_database() safely every time the app starts without errors
    or duplicate tables.
    """
    # Step 1: Ensure the data directory exists
    _DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Step 2: Open a connection to the database (creates it if missing)
    conn = sqlite3.connect(_DB_PATH)
    cursor = conn.cursor()

    try:
        # Step 3: Create each table
        cursor.execute(_CREATE_MONSTERS_TABLE)
        cursor.execute(_CREATE_ITEMS_TABLE)
        cursor.execute(_CREATE_LOCATIONS_TABLE)

        # Commit all changes at once
        conn.commit()
    finally:
        # Always close the connection when done
        conn.close()


def get_connection() -> sqlite3.Connection:
    """Return a new SQLite connection to the Rune AI database.

    Use this function whenever you need to query or modify data.
    Remember to call .commit() after writes and .close() when finished.

    Example::

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM monsters WHERE id = ?", (1,))
            row = cursor.fetchone()

    The returned connection is a standard sqlite3.Connection object.
    """
    return sqlite3.connect(_DB_PATH)


# ---------------------------------------------------------------------------
# Quick self-check — run `python -m data.database` to verify setup
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Database path: {_DB_PATH}")

    init_database()

    # Verify tables exist by listing them
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Tables created: {tables}")

    # Show column info for each table
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [(row[1], row[2]) for row in cursor.fetchall()]
        print(f"\n  {table}:")
        for col_name, col_type in columns:
            print(f"    - {col_name} ({col_type})")

    conn.close()
