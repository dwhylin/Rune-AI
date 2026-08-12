#!/usr/bin/env python3
"""
OSRS Monster Data Importer for Rune AI

This script fetches monster data from the OSRS Wiki and imports it into the
SQLite database. It uses the MediaWiki API to retrieve monster page names
from the "Category:Monsters" category, then fetches individual pages to extract
monster information.
"""

import sys
import urllib.request
import urllib.parse
import sqlite3
import time
import json
from typing import List, Dict, Optional

# Base URL for OSRS Wiki MediaWiki API
WIKI_API_BASE = "https://oldschool.runescape.wiki/api.php"

# Database connection helper
def get_db_connection():
    from data.database import _DB_PATH
    return sqlite3.connect(_DB_PATH)

# Headers to use for API requests
HEADERS = {
    "User-Agent": "RuneAI/1.0 (https://github.com/RuneAI)"
}

def fetch_monster_page_names() -> List[str]:
    """Fetch all monster page names from the OSRS Wiki Category:Monsters."""
    print("Fetching monster page names from OSRS Wiki...")
    
    # Initialize variables for pagination
    page_names = []
    continue_token = None
    
    while True:
        # Build API parameters
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": "Category:Monsters",
            "cmlimit": "500",  # Maximum allowed by API
            "format": "json"
        }
        
        # Add continuation token if we have one
        if continue_token:
            params["cmcontinue"] = continue_token
            
        # Make the request
        try:
            url = WIKI_API_BASE + "?" + urllib.parse.urlencode(params)
            request = urllib.request.Request(url, headers=HEADERS)
            response = urllib.request.urlopen(request)
            data = json.loads(response.read().decode('utf-8'))
            
            # Extract page names
            for member in data.get("query", {}).get("categorymembers", []):
                page_names.append(member["title"])
                
            # Check if there are more pages
            continue_token = data.get("continue", {}).get("cmcontinue")
            if not continue_token:
                break
                
        except Exception as e:
            print(f"Error fetching monster page names: {e}")
            break
    
    print(f"Found {len(page_names)} total monster pages.")
    return page_names

def fetch_monster_data_batch(page_titles: List[str]) -> List[Optional[Dict]]:
    """Fetch detailed data for multiple monster pages in a single API request."""
    try:
        # Build API parameters
        params = {
            "action": "query",
            "titles": "|".join(page_titles),
            "prop": "extracts",
            "explaintext": True,
            "format": "json"
        }
        
        # Make the request
        url = WIKI_API_BASE + "?" + urllib.parse.urlencode(params)
        request = urllib.request.Request(url, headers=HEADERS)
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        
        # Extract page content
        pages = data.get("query", {}).get("pages", {})
        if not pages:
            print(f"No pages found in API response for titles: {page_titles}")
            return [None] * len(page_titles)
            
        # Process pages - simplified approach
        results = []
        for title in page_titles:
            # Find the page with matching title
            page_data = pages.get(str(title), None) or pages.get(f"Page {title}", None)
            
            # If we found the page data and it has extract content
            if page_data and "extract" in page_data and page_data["extract"]:
                page_content = page_data["extract"]
                monster_data = parse_monster_page(page_content, title)
                results.append(monster_data)
            else:
                # Try to find by pageid instead
                page_id = None
                for page_id_key, page_value in pages.items():
                    if page_value.get("title") == title:
                        page_id = page_id_key
                        break
                        
                if page_id and "extract" in pages[page_id] and pages[page_id]["extract"]:
                    page_content = pages[page_id]["extract"]
                    monster_data = parse_monster_page(page_content, title)
                    results.append(monster_data)
                else:
                    print(f"No extract data for {title}")
                    results.append(None)
        
        return results
        
    except Exception as e:
        print(f"Error fetching batch data: {e}")
        return [None] * len(page_titles)

def parse_monster_page(content: str, title: str) -> Dict:
    """Parse the monster wiki page content to extract relevant fields."""
    # Initialize default values
    monster_info = {
        "name": title,
        "combat_level": None,
        "hitpoints": None,
        "attack_level": None,
        "strength_level": None,
        "defence_level": None,
        "magic_level": None,
        "ranged_level": None,
        "location": None,
        "wiki_url": f"https://oldschool.runescape.wiki/w/{title.replace(' ', '_')}"
    }
    
    # Simple parsing approach - look for key-value patterns
    lines = content.split('\n')
    
    # Look for combat level (e.g., "Combat level: 100")
    for line in lines:
        if "Combat level:" in line:
            try:
                monster_info["combat_level"] = int(line.split(":")[1].strip())
            except:
                pass
                
        elif "Hitpoints:" in line:
            try:
                monster_info["hitpoints"] = int(line.split(":")[1].strip())
            except:
                pass
                
        elif "Attack level:" in line:
            try:
                monster_info["attack_level"] = int(line.split(":")[1].strip())
            except:
                pass
                
        elif "Strength level:" in line:
            try:
                monster_info["strength_level"] = int(line.split(":")[1].strip())
            except:
                pass
                
        elif "Defence level:" in line:
            try:
                monster_info["defence_level"] = int(line.split(":")[1].strip())
            except:
                pass
                
        elif "Magic level:" in line:
            try:
                monster_info["magic_level"] = int(line.split(":")[1].strip())
            except:
                pass
                
        elif "Ranged level:" in line:
            try:
                monster_info["ranged_level"] = int(line.split(":")[1].strip())
            except:
                pass
                
        elif "Location:" in line:
            # Extract location from the line
            location_line = line.split(":", 1)
            if len(location_line) > 1:
                monster_info["location"] = location_line[1].strip()
    
    return monster_info

def insert_or_update_monster(monster_data: Dict) -> bool:
    """Insert or update a monster in the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Prepare the SQL statement
        sql = """
        INSERT OR REPLACE INTO monsters (
            name, combat_level, hitpoints, attack_level, strength_level,
            defence_level, magic_level, ranged_level, location, wiki_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Execute the insert or update
        cursor.execute(sql, (
            monster_data["name"],
            monster_data.get("combat_level"),
            monster_data.get("hitpoints"),
            monster_data.get("attack_level"),
            monster_data.get("strength_level"),
            monster_data.get("defence_level"),
            monster_data.get("magic_level"),
            monster_data.get("ranged_level"),
            monster_data.get("location"),
            monster_data.get("wiki_url")
        ))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error inserting/updating monster {monster_data['name']}: {e}")
        return False

def main():
    """Main function to run the monster importer."""
    print("Starting OSRS Monster Importer...")
    
    # Fetch all monster page names
    page_names = fetch_monster_page_names()
    
    if not page_names:
        print("No monster pages found.")
        return
        
    # Process monsters in batches to reduce API requests
    batch_size = 50  # Maximum allowed by MediaWiki API
    success_count = 0
    error_count = 0
    
    for i in range(0, len(page_names), batch_size):
        batch_page_names = page_names[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}: {len(batch_page_names)} monsters")
        
        # Fetch monster data for the batch
        batch_monster_data = fetch_monster_data_batch(batch_page_names)
        
        # Process each monster in the batch
        for monster_data in batch_monster_data:
            if monster_data:
                # Insert or update the monster
                if insert_or_update_monster(monster_data):
                    success_count += 1
                else:
                    error_count += 1
            else:
                error_count += 1
        
        # Add a small delay to be respectful to the API
        time.sleep(0.1)
    
    print(f"\nSuccessfully imported: {success_count} monsters")
    print(f"Errors: {error_count} monsters")

if __name__ == "__main__":
    main()