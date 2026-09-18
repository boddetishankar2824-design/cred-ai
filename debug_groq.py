import urllib.request
import urllib.error
import json

def test_groq():
    import os
    api_key = os.environ.get("GROQ_API_KEY", "")
    url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        data = json.loads(response.read().decode('utf-8'))
        for model in data.get('data', []):
            print(model['id'])
    except urllib.error.HTTPError as e:
        print(f"HTTPError {e.code}:", e.read().decode('utf-8'))
    except Exception as e:
        print("Other Exception:", str(e))

if __name__ == "__main__":
    test_groq()
