from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class OpenAIModule:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    async def get_response(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": message}],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
