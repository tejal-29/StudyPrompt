import json

from utils.gemini import client
import json
from .prompts import ROADMAP_PROMPT

def generate_roadmap(profile, goal):

    prompt = ROADMAP_PROMPT.format(
        role=profile.target_role,
        experience=profile.experience_level,
        hours=profile.daily_study_hours,
        goal=goal.title,
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )


    text = response.text

    text = text.replace(
        "```json",
        ""
    ).replace(
        "```",
        ""
    ).strip()

    return json.loads(text)