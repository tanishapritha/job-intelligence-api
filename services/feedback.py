from dotenv import load_dotenv
import os
from openai import OpenAI
import json

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

client = OpenAI(api_key=api_key)  # initialize once globally

async def generate_feedback(job_desc: str, resume_text: str) -> dict:
    """
    Uses GPT-4o-mini to generate:
    - missing keywords / concepts
    - suggestions to improve resume bullets
    """
    prompt = f"""
Job Description: {job_desc}
Resume Text: {resume_text}

Identify the important keywords/skills/technologies in the job description
that are **not effectively covered** in the resume. 
Also, provide concise suggestions to improve the resume to better match the JD.
Return a JSON with:
{{
    "missing_keywords": [...],
    "top_suggestions": [...]
}}
"""

    try:
        resp = await client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        text_resp = resp.choices[0].message.content
        feedback = json.loads(text_resp)
    except Exception:
        feedback = {"missing_keywords": [], "top_suggestions": []}

    return feedback
