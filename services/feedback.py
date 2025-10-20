from typing import Dict, List

def simple_missing_keywords(job_text: str, resume_text: str, top_n: int = 8) -> List[str]:
    """
    Super-simple heuristic to surface potential missing keywords:
    - tokenise job_text, remove short tokens, return tokens not in resume_text
    (This is only a placeholder for a real LLM-based feedback engine.)
    """
    import re
    def toks(s: str):
        return [t.lower() for t in re.findall(r"\w+", s) if len(t) > 3]
    job_tokens = toks(job_text)
    resume_tokens = set(toks(resume_text))
    missing = []
    for t in job_tokens:
        if t not in resume_tokens and t not in missing:
            missing.append(t)
            if len(missing) >= top_n:
                break
    return missing

def generate_feedback(job_text: str, resume_text: str) -> Dict:
    """
    Placeholder function that composes a small feedback object.
    Replace with LangChain/LLM logic for higher quality suggestions.
    """
    missing = simple_missing_keywords(job_text, resume_text)
    suggestion = "Consider adding the following keywords/skills in context of your experience: " + ", ".join(missing) if missing else "Resume appears to contain the core keywords."
    return {
        "match_score": None,
        "missing_keywords": missing,
        "suggestion": suggestion
    }
