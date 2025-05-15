from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class OpenAIModule:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def get_response(self, message: str) -> str:
        response = self.client.responses.create(
            model="gpt-4o-mini",
            input=message
        )
        return response.output_text
