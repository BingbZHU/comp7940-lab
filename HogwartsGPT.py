import requests
import configparser
import logging

class ChatGPT:
    def __init__(self, config):
        # Load API configuration
        api_key = config['CHATGPT']['API_KEY']
        base_url = config['CHATGPT']['BASE_URL']
        model = config['CHATGPT']['MODEL']
        api_ver = config['CHATGPT']['API_VER']

        # Build API request URL
        self.url = f'{base_url}/deployments/{model}/chat/completions?api-version={api_ver}'

        # Request headers
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "api-key": api_key,
        }

        # Hogwarts-themed system prompt, fully matches your bot positioning
        self.system_message = (
    'You are the exclusive intelligent navigation bot of Hogwarts School of Witchcraft and Wizardry. '
    'You only provide on-campus location navigation, route guidance, and location descriptions. '
    'Answer strictly based on a static knowledge base, never invent Hogwarts locations, routes, or information. '
    'Reply in a style that fits the user’s house: Gryffindor is brave and direct; Slytherin is elegant and reserved; '
    'Ravenclaw is concise and wise; Hufflepuff is gentle and patient. '
    'Use a light magical tone, keep answers concise and accurate, only output navigation-related content, '
    'and politely decline irrelevant questions.'
        )

    # Added support for passing user house tag for customized replies
    def submit(self, user_message: str, user_house: str = None):
        # 基础霍格沃茨导航提示词
        system_content = self.system_message
        # 若用户有学院，自动匹配对应语气（可选参数，None也不报错）
        if user_house:
            system_content += f"""
You are speaking to a {user_house} student. Strictly match your tone to this house:
- Gryffindor: Brave, direct, enthusiastic
- Slytherin: Cunning, elegant, concise
- Ravenclaw: Wise, logical, precise
- Hufflepuff: Warm, kind, patient
Only use this tone if the user's house is explicitly provided.
"""

        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_message}
        ]

        payload = {
            "messages": messages,
            "temperature": 1,
            "max_tokens": 300,
            "top_p": 1,
            "stream": False
        }

        response = requests.post(self.url, json=payload, headers=self.headers)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            logging.error(f"LLM Error: {response.status_code}, {response.text}")
            return "Magic signal lost, please try again later~"
    

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')    
    chatGPT = ChatGPT(config)
    while True:
        print('Hi, I am the Hogwarts Guide Bot, please enter your question: ', end='')
        response = chatGPT.submit(input())
        print(response)