import google.generativeai as genai

from decouple import config

from .prompts import AI_COACH_PROMPT

genai.configure(
    api_key=config("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


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

            remaining=analytics["total_tasks"] -
                      analytics["completed_tasks"],

            question=question,

        )

        response = model.generate_content(prompt)

        return response.text