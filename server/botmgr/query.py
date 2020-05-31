from .. import socketio
from flask_socketio import emit
from server.botmgr.conv_ai import ConversationalAiModel

class QueryHandler():

    def __init__(self):
        self.conv_ai = ConversationalAiModel('/home/jsnouffer/git/transfer-learning-conv-ai/model_checkpoint')

    def handle_query(self, text: str):
        response = self.conv_ai.process(text)
        emit('message', {'msg': response, 'sender': 'bot'}, broadcast=True)