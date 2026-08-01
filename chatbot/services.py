import google.generativeai as genai

from decouple import config

genai.configure(
    api_key=config("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


class ChatbotService:

    @staticmethod
    def ask(prompt):

        response = model.generate_content(prompt)

        return response.text