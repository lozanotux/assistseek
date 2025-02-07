import requests
import json
import re

# Define the prompt
prompt = 'hola'

# Local API endpoint
url = 'http://localhost:11434/api/generate'

# Needed headers
headers = {
    'Content-Type': 'application/json'
}

# Request payload
data = {
    'model': 'deepseek-r1:1.5b',
    'prompt': prompt,
    'stream': False,
    'options': {
        'temperature': 0
    }
}

# Process the response
response = requests.post(url, headers=headers, data=json.dumps(data))
print("Response:", response.text)
response_text = json.loads(response.text)['response']
filtered_text = re.sub(r'<think>.*?</think>', '', response_text, flags=re.DOTALL)
print(filtered_text.strip())