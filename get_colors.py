import urllib.request
import re
import collections
from urllib.parse import urljoin

url = 'https://www.credbuddha.com/'
# need to add user agent to avoid 403
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    css_links = re.findall(r'href=[\'"]([^\'"]+\.css)[?\'"]', html)
    colors = []
    
    # Also find colors in html inline styles
    colors.extend(re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}', html))
    
    for link in css_links:
        try:
            full_url = urljoin(url, link)
            req_css = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
            css = urllib.request.urlopen(req_css).read().decode('utf-8')
            colors.extend(re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}', css))
        except Exception as e:
            pass
            
    print("Most common colors:")
    for color, count in collections.Counter([c.lower() for c in colors]).most_common(30):
        print(f"{color}: {count}")
except Exception as e:
    print(f"Error: {e}")
