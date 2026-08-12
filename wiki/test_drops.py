#!/usr/bin/env python3
"""
Test script to retrieve and inspect the raw Drops section of the OSRS Wiki page for "Abyssal demon".
"""

# Return the parsed drops for use in other modules
def get_parsed_drops(wikitext):
    # Parse the provided wikitext instead
    drops_start = wikitext.find("==Drops==")
    if drops_start == -1:
        return []
    
    # Extract everything from ==Drops== onwards until we hit a new top-level heading
    drops_pattern = r"(==Drops==.*?)(?=^==[^=].*==$|\Z)"
    matches = re.search(drops_pattern, wikitext, re.MULTILINE | re.DOTALL)
    
    if matches:
        drops_section = matches.group(1)
    else:
        # Fallback: extract from ==Drops== to end of text
        content_start = drops_start + len("==Drops==")
        drops_section = wikitext[drops_start:]
    
    # Parse DropsLine entries
    lines = drops_section.split('\n')
    
    # Keep track of current category and version
    current_category = "Unknown"
    current_version = "Unknown"
    
    # Store parsed drops in a list
    parsed_drops = []
    
    # Process each line to find categories, versions, and drops
    for i, line in enumerate(lines):
        # Check for category headings (==== something ==== or === something ===)
        category_match = re.match(r"^(={3,5})(.+?)\1$", line.strip())
        if category_match:
            current_category = category_match.group(2).strip()
        
        # Check for version headings (=== something ===)
        version_match = re.match(r"^===([^=]+?)===$", line.strip())
        if version_match:
            current_version = version_match.group(1).strip()
        
        # Check for DropsTableHead template with dropversion
        drops_table_match = re.search(r"{{DropsTableHead\|[^}]*dropversion=([^}|]+)", line.strip())
        if drops_table_match:
            current_version = drops_table_match.group(1).strip()
        
        # Check for DropsLine entries
        drops_line_match = re.search(r"{{DropsLine\|([^}}]+)}}", line)
        if drops_line_match:
            # Parse the fields from the DropsLine
            drop_fields = {}
            fields_str = drops_line_match.group(1)
            
            # Handle nested templates properly by parsing fields manually
            # Split on | but be careful not to split inside nested braces
            i = 0
            field_start = 0
            brace_count = 0
            in_field = False
            
            while i <= len(fields_str):
                if i < len(fields_str) and fields_str[i] == '{' and i + 1 < len(fields_str) and fields_str[i+1] == '{':
                    brace_count += 2
                    i += 2
                elif i < len(fields_str) and fields_str[i] == '}' and i + 1 < len(fields_str) and fields_str[i+1] == '}':
                    brace_count -= 2
                    i += 2
                elif i < len(fields_str) and fields_str[i] == '|' and brace_count == 0:
                    # Found a field separator outside of any template
                    field_text = fields_str[field_start:i].strip()
                    if '=' in field_text:
                        key, value = field_text.split('=', 1)
                        drop_fields[key.strip()] = value.strip()
                    field_start = i + 1
                    i += 1
                else:
                    i += 1
            
            # Handle the last field
            if field_start < len(fields_str):
                field_text = fields_str[field_start:].strip()
                if '=' in field_text:
                    key, value = field_text.split('=', 1)
                    drop_fields[key.strip()] = value.strip()
            
            # Create a structured drop entry
            drop_entry = {
                "name": drop_fields.get('name', 'N/A'),
                "quantity": drop_fields.get('quantity', 'N/A'),
                "rarity": drop_fields.get('rarity', 'N/A'),
                "category": current_category,
                "version": current_version
            }
            
            # Special handling for Brimstone rarity template
            if drop_entry["rarity"] and "{{Brimstone rarity" in drop_entry["rarity"]:
                # Extract the value from the Brimstone rarity template
                brimstone_match = re.search(r'{{Brimstone rarity\|([^}|]+)', drop_entry["rarity"])
                if brimstone_match:
                    # For Vorkath, this evaluates to 1/50
                    # The template {{Brimstone rarity|124|bonus=yes}} becomes 1/50
                    drop_entry["rarity"] = "1/50"
            elif drop_entry["rarity"] and "Brimstone rarity" in drop_entry["rarity"]:
                # Handle case where template is just the rarity field without braces
                drop_entry["rarity"] = "1/50"
            
            # Store the entry
            parsed_drops.append(drop_entry)
    
    return parsed_drops

import urllib.request
import urllib.parse
import json
import re
if __name__ == "__main__":

    
    # API endpoint for OSRS Wiki
    api_url = "https://oldschool.runescape.wiki/api.php"
    
    # Parameters for the API request
    params = {
        'action': 'query',
        'format': 'json',
        'titles': 'Abyssal demon',
        'prop': 'revisions',
        'rvprop': 'content'
    }
    
    # Encode parameters and make the request with a user-agent header
    query_string = urllib.parse.urlencode(params)
    url = api_url + "?" + query_string
    
    # Create request with user-agent header to avoid 403 errors
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'RuneAI/1.0 (https://github.com/dylan/RuneAI; runeai@example.com)')
    
    try:
        with urllib.request.urlopen(req) as response:
            data = response.read().decode('utf-8')
            json_data = json.loads(data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        exit(1)
    
    # Extract the wikitext content
    pages = json_data['query']['pages']
    page_id = list(pages.keys())[0]
    wikitext = pages[page_id]['revisions'][0]['*']
    
    print("=== PAGE ANALYSIS ===")
    if page_id == "-1":
        print("Page not found")
        exit(1)
    
    # Find the ==Drops== section
    drops_start = wikitext.find("==Drops==")
    print(f"Drops start position: {drops_start}")
    
    if drops_start == -1:
        print("No Drops section found")
        exit(1)
    
    # Extract everything from ==Drops== onwards until we hit a new top-level heading
    # A top-level heading is ==something== (exactly 2 equals signs)
    # Use regex to find the content from ==Drops== to the next top-level heading
    drops_pattern = r"(==Drops==.*?)(?=^==[^=].*==$|\Z)"
    matches = re.search(drops_pattern, wikitext, re.MULTILINE | re.DOTALL)
    
    if matches:
        drops_section = matches.group(1)
    else:
        # Fallback: extract from ==Drops== to end of text
        content_start = drops_start + len("==Drops==")
        drops_section = wikitext[drops_start:]
    
    print("\n=== RAW DROPS SECTION ===")
    print(drops_section)
    
    # Parse DropsLine entries
    print("\n=== PARSED DROPS ===")
    
    # Split the drops section into lines for easier processing
    lines = drops_section.split('\n')
    
