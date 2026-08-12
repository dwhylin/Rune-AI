import urllib.request
import urllib.parse
import json

# API endpoint
url = "https://oldschool.runescape.wiki/api.php"

# Query parameters
params = {
    'action': 'query',
    'format': 'json',
    'list': 'categorymembers',
    'cmtitle': 'Category:Monsters',
    'cmlimit': 500  # Reasonable limit for each request
}

# Track all page titles
all_titles = []

# Continue making requests until no more pages
continue_token = None

while True:
    # Add continuation token if we have one
    if continue_token:
        params['cmcontinue'] = continue_token
    
    # Encode parameters
    query_string = urllib.parse.urlencode(params)
    full_url = url + "?" + query_string
    
    # Make the request with a User-Agent
    request = urllib.request.Request(full_url)
    request.add_header('User-Agent', 'OSRS-Monster-Scraper/1.0')
    
    try:
        # Send request and read response
        with urllib.request.urlopen(request) as response:
            data = response.read()
        
        # Parse JSON
        json_data = json.loads(data.decode('utf-8'))
        
        # Extract category members
        category_members = json_data['query']['categorymembers']
        
        # Add titles to our collection
        for member in category_members:
            all_titles.append(member['title'])
        
        # Check if there are more pages
        continue_token = json_data.get('continue', {}).get('cmcontinue')
        if not continue_token:
            break
            
    except Exception as e:
        print(f"Error: {e}")
        break

# Print results
print(f"Number of pages retrieved: {len(all_titles)}")

print("\nFirst 20 page titles:")
for i, title in enumerate(all_titles[:20]):
    print(f"{i+1:2d}. {title}")

print("\nLast 20 page titles:")
start_index = max(0, len(all_titles) - 20)
for i, title in enumerate(all_titles[start_index:], start_index + 1):
    print(f"{i:2d}. {title}")

print("\nAPI TEST SUCCESS")