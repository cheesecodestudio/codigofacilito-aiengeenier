import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_response_text(data):
    messages = []

    for output in data.get('output', []):
        if output.get('type') != 'message':
            continue

        for content in output.get('content', []):
            if content.get('type') == 'output_text':
                text = content.get('text')

                if text:
                    messages.append(text)

    return '\n'.join(messages)

def main():
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print('Foul..')
        return

    api_model = os.getenv('GROQ_API_MODEL')
    if not api_model:
        print('No Model')
        return

    print('Ready!!')

    response = requests.post(
        # 'https://api.openai.com/v1/responses', # OpenAI URL
        'https://api.groq.com/openai/v1/responses', # GROQ URL
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        # json={
        #     'model': api_model,
        #     'instructions': 'You are a senior developer',
        #     'input': 'Explain me about create a simple docker'
        # },
        json={
            'model': api_model,
            'input': [
                {
                    'role': 'system',
                    'content': 'You are a senior developer'
                },
                {
                    'role': 'user',
                    'content': 'Tell me the steps to create a simple Docker. Be direct and simple'
                }
            ]
        }
    )

    if response.status_code == 200:
        data = response.json()

        message = get_response_text(data)

        print('\n--- RESPONSE ---\n')
        print(message)
    else:
        print(f'Error status: {response.status_code}')
        print(response.json())

def getModels():
    api_key = os.environ.get("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/models"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    print(response.json())

if __name__ == '__main__':
    main()
    # getModels()