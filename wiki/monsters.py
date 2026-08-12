#!/usr/bin/env python3
"""
OSRS Wiki Monsters Parser for Abyssal demon page.
This script retrieves raw wikitext for the Abyssal demon page and parses
the Infobox Monster template and LocLine templates to extract structured data.
"""

import urllib.request
import urllib.parse
import json
import re
import sys
from .test_drops import get_parsed_drops

def fetch_raw_wikitext(page_title):
    """Fetch raw wikitext for a specific page."""
    url = "https://oldschool.runescape.wiki/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'titles': page_title,
        'prop': 'revisions',
        'rvprop': 'content'
    }
    
    # Build the full URL with query parameters
    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"
    
    # Create request with User-Agent header
    req = urllib.request.Request(full_url)
    req.add_header('User-Agent', 'OSRS-Monster-Parser/1.0')
    
    try:
        response = urllib.request.urlopen(req)
        data = response.read().decode('utf-8')
        parsed_data = json.loads(data)
        
        # Extract the wikitext
        pages = parsed_data['query']['pages']
        page_id = list(pages.keys())[0]
        if page_id != '-1':
            revisions = pages[page_id].get('revisions', [{}])
            if revisions:
                return revisions[0]['*']
    except Exception as e:
        print(f"Error fetching wikitext: {e}")
    
    return None

def extract_infobox_monster(wikitext):
    """Extract data from the Infobox Monster template."""
    # Pattern to match the Infobox Monster template
    infobox_pattern = r'\{\{Infobox Monster\s*(.*?)\}\}'
    match = re.search(infobox_pattern, wikitext, re.DOTALL | re.IGNORECASE)
    
    if not match:
        print("No Infobox Monster template found")
        return {}
    
    # Extract content inside the template
    content = match.group(1)
    
    # Parse key-value pairs more robustly - handling pipe syntax
    monster_data = {}
    
    # Split by newlines and process each line
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('|') and '=' in line:
            # Split on first '=' to separate key and value
            parts = line.split('=', 1)
            if len(parts) == 2:
                key = parts[0].strip()[1:]  # Remove the leading '|'
                value = parts[1].strip()
                
                # Clean up the value
                clean_value = value
                
                # Remove wiki link syntax like [[File:Abyssal demon.png]] or [[Some Page]]
                clean_value = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', clean_value)
                
                # Remove any remaining brackets
                clean_value = re.sub(r'[\[\]]', '', clean_value)
                
                if key and clean_value:
                    monster_data[key.lower()] = clean_value
    
    return monster_data

def extract_loc_lines(wikitext):
    """Extract location names from LocLine templates."""
    loc_lines = []
    
    # Pattern to match LocLine templates
    pattern = r'\{\{LocLine\s*(.*?)\}\}'
    matches = re.findall(pattern, wikitext, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        # Parse key-value pairs in the LocLine template
        lines = match.strip().split('|')
        for line in lines:
            line = line.strip()
            if line.startswith('location ='):
                # Extract the value after 'location ='
                location = line.split('=', 1)[1].strip()
                # Remove wiki link syntax [[...]]
                location = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', location)
                # Remove wiki template syntax like {{Fairycode}}
                location = re.sub(r'\{\{[^}]*\}\}', '', location)
                # Clean up any remaining parentheses that might contain template-like content
                location = re.sub(r'\s*\([^)]*\)', '', location)
                # Clean up trailing parentheses and any leftover template-like content
                location = re.sub(r'\s*\([^)]*\)$', '', location)
                # Remove any remaining brackets or artifacts
                location = re.sub(r'[\[\]]', '', location)
                # Strip leading/trailing whitespace
                location = location.strip()
                # Final cleanup: remove any remaining template-like content at the end
                location = re.sub(r'\{\{[^}]*$', '', location)
                # Remove any trailing parentheses that might contain template-like content
                location = re.sub(r'\s*\([^)]*\{\{[^}]*\}\)', '', location)
                # Remove any remaining trailing parentheses with content
                location = re.sub(r'\s*\([^)]*\)$', '', location)
                # Clean up any remaining artifacts like ' (' at the end
                location = re.sub(r'\s+\(.*$', '', location)
                # Additional cleanup for edge cases with template content - ensure all remaining template fragments are removed
                location = re.sub(r'\{\{[^}]*\}\}?', '', location)
                if location:  # Only add non-empty locations
                    loc_lines.append(location)
    
    return loc_lines

def main():
    """Main function to parse monster data."""
    # Get monster name from command line or default to "Abyssal demon"
    monster_name = sys.argv[1] if len(sys.argv) > 1 else "Abyssal demon"
    
    print(f"Parsing {monster_name} page from OSRS Wiki...")
    
    # Fetch raw wikitext for the specified monster
    wikitext = fetch_raw_wikitext(monster_name)
    
    if not wikitext:
        print(f"Failed to fetch wikitext for {monster_name}")
        return
    
    print(f"Retrieved wikitext of {len(wikitext)} characters")
    
    # Extract infobox monster data
    monster_data = extract_infobox_monster(wikitext)
    
    # Extract location lines
    locations = extract_loc_lines(wikitext)
    
    # Get parsed drops
    drops = get_parsed_drops(wikitext)
    
    # Print the parsed monster data as readable JSON
    print("\nParsed Monster Data:")
    print(json.dumps(monster_data, indent=2))
    
    # Print locations
    print(f"\nLocations ({len(locations)} total):")
    for i, location in enumerate(locations[:20]):
        print(f"  {i+1}. {location}")
    
    if len(locations) > 20:
        print("  ... and {} more locations".format(len(locations) - 20))
    
    # Print drops
    print(f"\nDrops ({len(drops)} total):")
    for drop in drops:
        category = drop['category'].replace(' (Post-quest)', '')
        print(f"  {drop['name']} ({drop['quantity']}) - {drop['rarity']} in {category}")
    
    # Add drops to monster data
    monster_data["drops"] = drops
    
    # Print summary
    print(f"\nSummary:")
    print(f"  Total fields extracted: {len(monster_data)}")
    print(f"  Total locations found: {len(locations)}")

if __name__ == "__main__":
    main()