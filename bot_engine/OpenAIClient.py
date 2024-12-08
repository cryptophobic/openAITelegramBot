import os

import openai
from dotenv import load_dotenv, find_dotenv


class OpenAIClient:
    def __init__(self):
        load_dotenv(find_dotenv(), override=True)
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.client = openai.OpenAI()

    def print_all_models(self):
        for model in self.client.models.list():
            print(model)
