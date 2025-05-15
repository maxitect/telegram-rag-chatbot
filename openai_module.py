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
        context = self.chroma.query_documents(message)

        prompt = f"""
        You are a helpful assistant. Use the following context to answer the
        user's question. If the context doesn't contain relevant information,
        say so.

Context:
{context}

User question: {message}

Answer:"""

        response = self.client.responses.create(
            model="gpt-4.1-nano",
            input=prompt
        )
        return response.output_text
