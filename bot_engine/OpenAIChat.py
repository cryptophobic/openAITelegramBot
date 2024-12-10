from collections import deque
from typing import List, Dict, Tuple, Deque

import openai
from openai.types.chat import ChatCompletion


class OpenAIChat:
    def __init__(self, client: openai.OpenAI):
        self.client = client
        self.system_role = 'you\'re sarcastic assistant with dark sense of humor'
        self.custom_role: Dict[str, str] = {}
        # self.model = 'o1-preview-2024-09-12'
        self.model = 'gpt-3.5-turbo'
        self.temperature=1 # 1 by default
        self.seed=None # to use deterministic outputs use same seed value
        self.top_p=None # 1 by default
        self.max_tokens=None #
        self.n=1
        self.stop=None
        self.frequency_penalty=None # between -2 and 2, default 0
        self.presence_penalty=None # between -2 and 2, default 0
        self.last_response=None
        self.last_request: str=''
        self.user_history: [Dict[str, Deque[Tuple[str, str]]]]={}

    def set_custom_role(self, user, value):
        self.user_history.pop(user, None)
        self.custom_role[user] = value

    def get_custom_role(self, user: str):
        return self.system_role if user not in self.custom_role else self.custom_role[user]

    def get_last_response(self, user: str) -> str:
        return self.user_history[user][-1][1] if user in self.user_history else ''
        # return self.last_response.choices[n].message.content if isinstance(self.last_response, ChatCompletion) else ''

    def execute_chat_completion(self, user_prompt, user: str = None):
        messages_param = [
            {'role': 'system', 'content': self.get_custom_role(user)},
        ]

        if user in self.user_history:
            for question, answer in self.user_history[user]:
                messages_param.append({'role': 'user', 'content': question[:1000]})
                messages_param.append({'role': 'assistant', 'content': answer[:1000]})

        messages_param.append({'role': 'user', 'content': user_prompt})

        params = {
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'n': self.n,
            'top_p': self.top_p,
            'frequency_penalty': self.frequency_penalty,
            'presence_penalty': self.presence_penalty,
            'model': self.model,
            'messages': messages_param,
            'seed': self.seed,
            'stop': self.stop,
        }

        params = {key: value for (key, value) in params.items() if value is not None}
        print(params)

        self.last_response = self.client.chat.completions.create(**params)
        if not user in self.user_history:
            self.user_history[user] = deque(maxlen=10)

        self.user_history[user].append((user_prompt, self.last_response.choices[0].message.content))
