import urllib.request
import re

url = 'https://www.credbuddha.com/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    match = re.search(r'<img[^>]+src=[\'"]([^\'"]*logo[^\'"]*)[\'"]', html, re.IGNORECASE)
    if match:
        print(match.group(1))
    else:
        print("Logo not found")
except Exception as e:
    print(f"Error: {e}")
