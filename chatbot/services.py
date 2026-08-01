from utils.gemini import client
from google.genai import types

class ChatbotService:

    @staticmethod
    def ask(prompt):

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="text/plain"),
        )

        return response.text
