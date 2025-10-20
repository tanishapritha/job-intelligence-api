from fastapi import APIRouter, HTTPException
from schemas.resume import AnalyzeRequest, AnalyzeResponse
from services.embeddings import embed_one
from services.similarity import cosine_similarity, hybrid_score, extract_keywords, keyword_overlap_score
from services.feedback import generate_feedback
from utils.logger import logger

router = APIRouter(tags=["Resume Analyzer"])

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    try:
        resume_emb = await embed_one(req.resume_text)
        job_emb = await embed_one(req.job_description)

        emb_score = cosine_similarity(resume_emb, job_emb)
        combined = hybrid_score(emb_score, req.job_description, req.resume_text)

        job_keywords = extract_keywords(req.job_description, top_n=12)
        resume_keywords = extract_keywords(req.resume_text, top_n=12)
        kw_overlap = keyword_overlap_score(req.job_description, req.resume_text)

        # Correctly await the coroutine
        feedback = await generate_feedback(req.job_description, req.resume_text)

        suggestion_list = feedback.get("top_suggestions") or feedback.get("rewrite_bullets") or []
        suggestion_str = "; ".join(suggestion_list)

        response = AnalyzeResponse(
            similarity_score=round(combined, 4),
            resume_summary=(req.resume_text.strip()[:240] + ("..." if len(req.resume_text) > 240 else "")),
            job_summary=(req.job_description.strip()[:240] + ("..." if len(req.job_description) > 240 else "")),
            missing_keywords=feedback.get("missing_keywords", []),
            suggestion=suggestion_str,
            debug={
                "emb_score": round(emb_score, 4),
                "keyword_overlap": round(kw_overlap, 4),
                "job_keywords": job_keywords,
                "resume_keywords": resume_keywords,
                "llm_match_score": feedback.get("match_score"),
            },
        )
        return response

    except Exception as e:
        logger.exception(f"analyze failed: {e}")
        raise HTTPException(status_code=500, detail="internal error")
