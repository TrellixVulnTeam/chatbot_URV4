import os

from .. import socketio
from flask_socketio import emit
from .open_ai.conv_ai import ConversationalAiModel

class QueryHandler():

    handlers: list = []

    def __init__(self):
        self.openai_enabled: bool = os.getenv('openai.enabled') == 'true'

        if self.openai_enabled:
            self.conv_ai = ConversationalAiModel(os.getenv('openai_model'))

    def handle_query(self, text: str):
        response = ""
        
        if self.openai_enabled:
            response = self.conv_ai.process(text)

        emit('message', {'msg': response, 'sender': 'bot'}, broadcast=True)