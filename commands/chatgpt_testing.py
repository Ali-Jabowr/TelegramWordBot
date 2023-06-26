import requests

API_ENDPOINT = 'https://api.openai.com/v1/chat/completions'
API_KEY = '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'
MODEL_ID = 'gpt-3.5-turbo'

def test_chatgpt_api():
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': MODEL_ID,
        'messages': [{'role': 'system', 'content': 'Test message'}]
    }
    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    
    if response.status_code == 200:
        print("API is working normally.")
    else:
        print("API request failed. Status code:", response.status_code)
        print("Response:", response.json())

# Call the function to test the API
test_chatgpt_api()