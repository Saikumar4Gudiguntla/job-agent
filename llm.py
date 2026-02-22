import re
from typing import Dict, List

STOPWORDS = {
    "the", "and", "a", "an", "to", "of", "in", "for", "on", "with", "as", "is", "are",
    "was", "were", "this", "that", "it", "be", "by", "or", "from", "at", "we", "you",
    "your", "our", "their"
}


def _keywords(text: str, top_n: int = 20) -> List[str]:
    # simple keyword extractor (works offline)
    words = re.findall(r"[A-Za-z][A-Za-z0-9\-\+\.]{1,}", (text or "").lower())
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    ranked = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return [w for w, _ in ranked[:top_n]]


def generate_job_package(resume_text: str, job_description_text: str, role_title: str) -> Dict:
    jd_kw = _keywords(job_description_text, top_n=25)
    resume_kw = set(_keywords(resume_text, top_n=40))

    missing = [k for k in jd_kw if k not in resume_kw]

    bullets = [
        f"Built workflow automation aligned to {role_title} requirements, improving delivery speed and output consistency.",
        "Extracted ATS keywords from job descriptions and generated role-aligned resume bullets for better screening outcomes.",
        "Created recruiter-ready outreach messages and interview talking points based on resume + job requirements."
    ]

    recruiter_message = (
        f"Hi Recruiter,\n\n"
        f"I'm interested in the {role_title} role. My background aligns strongly with "
        f"{', '.join(jd_kw[:6])}. I’d love to share a quick summary of how I can help your team.\n\n"
        f"Are you open to a short 10-minute chat this week?\n\n"
        f"Thanks,\nSai"
    )

    talking_points = [
        f"Walk through 1–2 projects that match {role_title} responsibilities.",
        "Explain how you ensure correctness, privacy, and clarity when building data/health workflows.",
        "Describe a debugging story: issue → root cause → fix → prevention (tests/validation).",
        "Show how you convert requirements into measurable deliverables and results.",
        "Explain how you communicate tradeoffs clearly to stakeholders."
    ]

    return {
        "tailored_resume_bullets": bullets,
        "ats_keywords": jd_kw,
        "missing_keywords": missing[:15],
        "recruiter_message": recruiter_message,
        "interview_talking_points": talking_points
    }
