import dialogflow
import os
import uuid
import google.protobuf as pf
from google.api_core.exceptions import InvalidArgument

DIALOGFLOW_PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('datamining-193201')
SESSION_ID = str(uuid.uuid4())


class DialogFlowResults():
    def __init__(self, response):
        self.response: dict = pf.json_format.MessageToDict(response)
        self.intent: str = response.query_result.intent.display_name
        self.fulfillment_text = response.query_result.fulfillment_text
        self.is_fallback: bool = response.query_result.intent.is_fallback == 'true'

class DialogFlowHandler():

    def __init__(self):
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    def process(self, raw_text: str) -> DialogFlowResults:
        text_input = dialogflow.types.TextInput(text=raw_text, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            response = self.session_client.detect_intent(session=self.session, query_input=query_input)
            return DialogFlowResults(response)
        except InvalidArgument:
            return None