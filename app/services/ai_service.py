from typing import List, Dict, Any
from ..config import settings
from google import genai
from fastapi import HTTPException
import json
from datetime import datetime



GOOGLE_GENAI_API_KEY = settings.GOOGLE_API_KEY.get_secret_value() if settings.GOOGLE_API_KEY else None
if GOOGLE_GENAI_API_KEY:
    client = genai.Client(api_key=GOOGLE_GENAI_API_KEY)



def generate_habits(goal: str) -> List[Dict[str, Any]]:
    if not GOOGLE_GENAI_API_KEY:
        return [
            {"title": "Drink 2L Water", "difficulty": "Easy"},
            {"title": "Read 15 mins", "difficulty": "Medium"},
            {"title": "Walk 5k steps", "difficulty": "Medium"},
            {"title": "Meditate 5 mins", "difficulty": "Easy"},
            {"title": "Journaling", "difficulty": "Hard"},
            {"title": "No Sugar", "difficulty": "Medium"},
            {"title": "Sleep 8hrs", "difficulty": "Hard"},
            {"title": "Stretch", "difficulty": "Easy"},
            {"title": "Plan Day", "difficulty": "Easy"},
            {"title": "Deep Work 1hr", "difficulty": "Hard"}
        ]
    
    try:
        res = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents=f"""Generate 10 specific, small atomic hard dedicated habits for a user whose goal is: "{goal}".
        Return ONLY a raw JSON array of objects. Each object must have 'title' (string, max 5 words).
        Do not use markdown formatting."""
        )
        text = res.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}") 
    

def generate_summary_from_tasks(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not GOOGLE_GENAI_API_KEY:
        return {"summary": "Please configure GOOGLE_API_KEY to see your AI summary.", "score": 0}

    total = len(tasks)
    completed = len([t for t in tasks if t.get("completed")])
    overdue = len([t for t in tasks if not t.get("completed") and t.get("deadline") < datetime.utcnow().isoformat()])
    score = int((completed / total) * 100) if total > 0 else 0

    try:
        res = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents=
            f"""Analyze these stats: Total={total}, Completed={completed}, Overdue={overdue}, Score={score}."
            "Write a two-sentence encouraging summary that addresses the user and suggests improvements if overdue>0."""
        )
        return {'summary': res.text.strip(), 'score': score}
    except Exception:
        raise HTTPException(status_code=500, detail="AI summary generation failed")