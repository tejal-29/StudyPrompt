from google import genai
from decouple import config

client = genai.Client(
    api_key=config("GEMINI_API_KEY")
)

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Say Hello"
)

print(response.text)