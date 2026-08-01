import json

import google.generativeai as genai

from decouple import config

from .prompts import ROADMAP_PROMPT


genai.configure(
    api_key=config("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_roadmap(profile, goal):

    prompt = ROADMAP_PROMPT.format(
        role=profile.target_role,
        experience=profile.experience_level,
        hours=profile.daily_study_hours,
        goal=goal.title,
    )

    response = model.generate_content(prompt)

    return json.loads(response.text)