# modules/shortlist.py
from config import get_chroma, LLM


def generate_llm_response(job_description, resume_text):
    resume_preview = resume_text[:2000]   # truncate safely

    prompt = f"""
You are an expert HR recruiter.
Compare the Resume and Job Description.

Job Description:
{job_description}

Resume:
{resume_preview}

Explain clearly:
- Why this resume is relevant
- Key matching skills
- Experience alignment
- Short suitability summary
"""

    response = LLM.invoke(prompt)
    return response.content


def shortlist_resumes(job_description, k):
    chroma = get_chroma()

    result = chroma.similarity_search(
        query=job_description,
        k=k
    )

    shortlisted = []

    for r in result:
        explanation = generate_llm_response(
            job_description,
            r.page_content
        )

        shortlisted.append({
            "file": r.metadata["file_name"],
            "pages": r.metadata["pages"],
            "content": r.page_content[:400],
            "llm_reason": explanation       # <-- IMPORTANT
        })

    return shortlisted
