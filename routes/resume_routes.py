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
        # compute embeddings (async; uses redis cache internally)
        resume_emb = await embed_one(req.resume_text)
        job_emb = await embed_one(req.job_description)

        # emb similarity
        emb_score = cosine_similarity(resume_emb, job_emb)

        # hybrid score (emb + keyword overlap)
        combined = hybrid_score(emb_score, req.job_description, req.resume_text)

        # keyword lists for transparency
        job_keywords = extract_keywords(req.job_description, top_n=12)
        resume_keywords = extract_keywords(req.resume_text, top_n=12)
        kw_overlap = keyword_overlap_score(req.job_description, req.resume_text)

        # LLM-based feedback (async). returns structured json
        feedback = await generate_feedback(req.job_description, req.resume_text, combined)

        response = AnalyzeResponse(
            similarity_score=round(combined, 4),
            resume_summary=(req.resume_text.strip()[:240] + ("..." if len(req.resume_text) > 240 else "")),
            job_summary=(req.job_description.strip()[:240] + ("..." if len(req.job_description) > 240 else "")),
            missing_keywords=feedback.get("missing_keywords", []),
            suggestion="; ".join(feedback.get("top_suggestions", [])) or feedback.get("rewrite_bullets", []),
            debug={
                "emb_score": round(emb_score, 4),
                "keyword_overlap": round(kw_overlap, 4),
                "job_keywords": job_keywords,
                "resume_keywords": resume_keywords,
                "llm_match_score": feedback.get("match_score")
            }
        )
        return response
    except Exception as e:
        logger.exception("analyze failed")
        raise HTTPException(status_code=500, detail="internal error")
