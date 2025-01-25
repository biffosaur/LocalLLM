import requests
import json

API_KEY = ""  # The key printed when starting the server
URL = "https://192.168.86.105:5001/api/chat"

response = requests.post(
    URL,
    json={
        "model": "llama3.2",
        "messages": [
            {
                "role": "user",
                "content": "Good morning, i'm testing out connecting from one pc to another!"
            }
        ],
        "stream": False  # Explicitly request non-streaming response
    },
    headers={"X-API-Key": API_KEY},
    verify=False
)

# Print the raw response first for debugging
print("Raw response:", response.text)

# Try to parse the response
try:
    full_text = ""
    # Handle both streaming and non-streaming responses
    if response.headers.get('content-type') == 'text/event-stream':
        for line in response.text.split('\n'):
            if line.strip():
                try:
                    json_response = json.loads(line)
                    if 'message' in json_response and 'content' in json_response['message']:
                        full_text += json_response['message']['content']
                except json.JSONDecodeError:
                    continue
        print("Full response:", full_text)
    else:
        # Try regular JSON response
        json_response = response.json()
        print("JSON response:", json_response)
except Exception as e:
    print("Error parsing response:", str(e))
