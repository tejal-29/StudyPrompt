ROADMAP_PROMPT = """
You are an AI Career Mentor.

Generate a personalized learning roadmap.

Return ONLY valid JSON.

JSON Format

{
 "roadmap_title":"",
 "description":"",
 "total_weeks":0,
 "phases":[
   {
      "phase_name":"",
      "week_number":1,
      "estimated_days":7,
      "topics":[
         {
            "topic_name":"",
            "difficulty":"",
            "estimated_hours":0,
            "resources":""
         }
      ]
   }
 ]
}

Student Information

Role : {role}

Experience : {experience}

Study Hours : {hours}

Goal : {goal}
"""