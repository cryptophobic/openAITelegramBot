from bot_engine.OpenAIImages import OpenAIImages
from bot_engine.OpenAIClient import OpenAIClient


class Images:
    def __init__(self, context: str = ''):
        self.context = context
        self.client = OpenAIClient()
        self.images = OpenAIImages(self.client.client)

    def set_request(self, request) -> None:
        self.images.execute_image_generating(request)

    def get_response(self) -> str:
        url = self.images.get_last_response()
        return self.images.save_url(url)
