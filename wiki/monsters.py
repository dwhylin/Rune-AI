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
    'cmlimit': 10
}

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
    
    # Print results
    print(f"Number of returned category members: {len(category_members)}")
    
    for member in category_members:
        print(member['title'])
    
    print("API TEST SUCCESS")
    
except Exception as e:
    print(f"Error: {e}")