import urllib.request
import re

url = "https://dribbble.com/shots/24805763-Farm-Management-System-Client-Dashboard"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
        # Searching for typical high-res image URLs in dribbble shots
        # They often look like https://cdn.dribbble.com/userupload/...
        urls = re.findall(r'https://cdn\.dribbble\.com/userupload/[^"\'\s]+', html)
        if urls:
            # Pick the longest URL or the first one containing 'webp' or 'png'
            best_url = urls[0]
            print("Found image URLs:", len(urls))
            print("Using:", best_url)
            
            img_req = urllib.request.Request(best_url, headers=headers)
            with urllib.request.urlopen(img_req) as img_resp:
                with open('dribbble_shot.jpg', 'wb') as f:
                    f.write(img_resp.read())
            print("Successfully downloaded to dribbble_shot.jpg")
        else:
            print("Could not find any cdn.dribbble.com/userupload URLs")
except Exception as e:
    print("Error:", e)
