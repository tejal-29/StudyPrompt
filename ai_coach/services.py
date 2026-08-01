from google import genai
from decouple import config
from google.genai import types
from .prompts import AI_COACH_PROMPT

client = genai.Client(api_key=config("GEMINI_API_KEY"))


class AICoachService:

    @staticmethod
    def ask(profile, goal, analytics, question):

        prompt = AI_COACH_PROMPT.format(
            role=profile.target_role,
            experience=profile.experience_level,
            study_hours=profile.daily_study_hours,
            goal=goal.title,
            progress=analytics["progress"],
            completed=analytics["completed_tasks"],
            remaining=analytics["total_tasks"] - analytics["completed_tasks"],
            question=question,
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="text/plain"),
        )

        return response.text
