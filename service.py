from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class AzureOpenAIService:
    def __init__(self):
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        
        # Initialize the AzureOpenAI client
        self.client = AzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            api_version="2023-03-15-preview"
        )

    def get_llm_response(self, user_message):
        # Use the client to get a chat completion response
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()