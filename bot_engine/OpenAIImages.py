import shutil
import time

import requests
import openai
from openai.types import ImagesResponse


class OpenAIImages:
    def __init__(self, client: openai.OpenAI):
        self.client = client
        self.model = 'dall-e-3'
        self.style='vivid'
        self.size='1024x1024'
        self.quality='standard'
        self.n=1
        self.last_response=None

    def get_last_response(self, n=0) -> str :
        return self.last_response.data[n].url if isinstance(self.last_response, ImagesResponse) else ''

    def execute_image_variation(self, file_name):
        image = open(f'generated/{file_name}', 'rb')
        params = {
            'image': image,
            'n': self.n,
            'size': self.size,
        }
        params = {key: value for (key, value) in params.items() if value is not None}
        self.last_response = self.client.images.create_variation(**params)

    def save_url(self, url):
        image_resource = requests.get(url)
        file_name = f'generated/{int(time.time())}.png'
        if image_resource.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(image_resource.content)
        else:
            print("Error accessing image")

        return file_name

    def save_last_response(self, n=0) -> str :
        return self.save_url(self.get_last_response(n))

    def execute_image_editing(self, file_name, mask_file_name, user_prompt):
        image = open(f'generated/{file_name}', 'rb')
        mask = open(f'generated/{mask_file_name}', 'rb')

        params = {
            'image': image,
            'mask': mask,
            'prompt': user_prompt,
            'n': self.n,
            'size': self.size,
        }

        params = {key: value for (key, value) in params.items() if value is not None}
        self.last_response = self.client.images.edit(**params)


    def execute_image_generating(self, user_prompt):
        params = {
            'model': self.model,
            'prompt': user_prompt,
            'style': self.style,
            'size': self.size,
            'quality': self.quality,
            'n': self.n,
        }

        params = {key: value for (key, value) in params.items() if value is not None}
        self.last_response = self.client.images.generate(**params)