#!/usr/bin/env python3
"""
Diagnostic script to check the current state of the monsters table in Rune AI's SQLite database.
"""

import sqlite3
from data.database import _DB_PATH

def check_monsters_database():
    """Check the monsters table for diagnostic information."""
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        
        # Get total number of rows
        cursor.execute("SELECT COUNT(*) FROM monsters")
        total_count = cursor.fetchone()[0]
        
        # Get first 30 monster names alphabetically
        cursor.execute("SELECT name FROM monsters ORDER BY name ASC LIMIT 30")
        first_30 = [row[0] for row in cursor.fetchall()]
        
        # Get last 30 monster names alphabetically
        cursor.execute("SELECT name FROM monsters ORDER BY name DESC LIMIT 30")
        last_30 = [row[0] for row in cursor.fetchall()]
        
        # Count records with missing combat level
        cursor.execute("SELECT COUNT(*) FROM monsters WHERE combat_level IS NULL OR combat_level = ''")
        missing_combat = cursor.fetchone()[0]
        
        # Count records with missing hitpoints
        cursor.execute("SELECT COUNT(*) FROM monsters WHERE hitpoints IS NULL OR hitpoints = ''")
        missing_hitpoints = cursor.fetchone()[0]
        
        # Count records with missing location
        cursor.execute("SELECT COUNT(*) FROM monsters WHERE location IS NULL OR location = ''")
        missing_location = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"Total number of rows in the monsters table: {total_count}")
        print(f"First 30 monster names alphabetically: {first_30}")
        print(f"Last 30 monster names alphabetically: {last_30}")
        print(f"Records with missing combat level: {missing_combat}")
        print(f"Records with missing hitpoints value: {missing_hitpoints}")
        print(f"Records with missing location: {missing_location}")
        
    except Exception as e:
        print(f"Error checking database: {e}")

if __name__ == "__main__":
    check_monsters_database()