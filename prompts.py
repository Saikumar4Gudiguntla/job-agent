SYSTEM = """You are a senior US-based recruiter + ATS optimization expert.
Be precise. No fluff. Output must be ready to paste into a resume or LinkedIn message.
Never invent experience. Only rewrite/reframe what exists in resume_text."""

KEYWORDS_PROMPT = """
Extract the 20 most important ATS keywords/phrases from the job description.
Return ONLY a JSON list of strings.
Job description:
{jd}
"""

BULLETS_PROMPT = """
Create 6 ATS-optimized resume bullets for the role: {role_title}.
Rules:
- Use ONLY information present in resume_text (no fabrication).
- Each bullet: 1 line, starts with a strong action verb, includes a metric if resume provides one.
- Align bullets to the job description priorities.
Return ONLY a JSON list of 6 strings.

resume_text:
{resume}

job_description:
{jd}
"""

RECRUITER_PROMPT = """
Write a short recruiter outreach message (max 120 words) for {company} / {role_title}.
Rules:
- Friendly, direct, confident.
- Mention 2 strongest matches from resume to JD.
- End with a simple ask for a 10-min chat.
Return plain text only.

resume_text:
{resume}

job_description:
{jd}
"""

TALKING_POINTS_PROMPT = """
Generate 5 interview talking points tailored to {role_title}.
Rules:
- Only use resume facts.
- Each point: 1 sentence, STAR-style hook (Situation/Task/Action/Result).
Return ONLY a JSON list of 5 strings.

resume_text:
{resume}

job_description:
{jd}
"""
