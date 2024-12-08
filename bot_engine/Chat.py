from bot_engine.OpenAIChat import OpenAIChat
from bot_engine.OpenAIClient import OpenAIClient


class Chat:
    def __init__(self, context: str = ''):
        self.context = context
        self.client = OpenAIClient()
        self.chat = OpenAIChat(self.client.client)

    def set_request(self, request, user) -> None:
        self.chat.execute_chat_completion(request, user)

    def get_response(self, user) -> str:
        return self.chat.get_last_response(user)
