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

# Filter out titles that begin with "Category:"
original_count = len(all_titles)
filtered_titles = [title for title in all_titles if not title.startswith("Category:")]


# Now check metadata for the filtered titles
print("Checking page metadata for filtered titles...")
print(f"Total candidates: {len(filtered_titles)}")

# Batch processing to avoid URI too long errors
batch_size = 50
total_pages = 0
missing_pages = 0
namespace_0_pages = 0
non_namespace_0_pages = 0
namespace_0_titles = []

# Process in batches
for i in range(0, len(filtered_titles), batch_size):
    batch = filtered_titles[i:i + batch_size]
    
    # Prepare parameters for checking page metadata
    metadata_params = {
        'action': 'query',
        'format': 'json',
        'titles': '|'.join(batch),
        'prop': 'info',
        'inprop': 'namespace|missing'
    }
    
    # Encode parameters
    metadata_query_string = urllib.parse.urlencode(metadata_params)
    metadata_full_url = url + "?" + metadata_query_string
    
    # Make the request with a User-Agent
    metadata_request = urllib.request.Request(metadata_full_url)
    metadata_request.add_header('User-Agent', 'OSRS-Monster-Scraper/1.0')
    
    try:
        # Send request and read response
        with urllib.request.urlopen(metadata_request) as response:
            data = response.read()
        
        # Parse JSON
        metadata_json_data = json.loads(data.decode('utf-8'))
        
        # Extract pages information
        pages = metadata_json_data['query']['pages']
        
        # Process each page in this batch
        for page_id, page_info in pages.items():
            if page_id == '-1':
                # This means the page was not found
                missing_pages += 1
            else:
                # Page exists
                if 'missing' in page_info:
                    missing_pages += 1
                else:
                    # Page exists, check namespace
                    namespace = page_info.get('ns', -1)
                    if namespace == 0:
                        namespace_0_pages += 1
                        if len(namespace_0_titles) < 20:
                            namespace_0_titles.append(page_info['title'])
                    else:
                        non_namespace_0_pages += 1
        
        total_pages += len(pages)
        
    except Exception as e:
        print(f"Error processing batch {i//batch_size + 1}: {e}")
        break

# Print summary
print(f"Pages found: {total_pages - missing_pages}")
print(f"Pages missing: {missing_pages}")
print(f"Pages in namespace 0: {namespace_0_pages}")
print(f"Pages not in namespace 0: {non_namespace_0_pages}")

print("\nFirst 20 namespace 0 titles:")
for i, title in enumerate(namespace_0_titles, 1):
    print(f"{i:2d}. {title}")
    
print("\nAPI TEST SUCCESS")