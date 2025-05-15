from openai import OpenAI
import os
from dotenv import load_dotenv
from chroma_module import ChromaModule

load_dotenv()


class OpenAIModule:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.chroma = ChromaModule()

    def get_response(self, message: str) -> str:
        context = self.chroma.get_context_for_query(message)

        prompt = f"""
        Based on the context provided below, extracted from the results from
        this query: {message}, answer the user's question. If the context
        doesn't contain relevant information, say so. Do not try to make
        anything up or infer additional information than the context provided.

Context:
{context}
"""

        response = self.client.responses.create(
            model="gpt-4.1-nano",
            input=prompt
        )
        return response.output_text
