# modules/shortlist.py
from config import get_chroma

def shortlist_resumes(job_description, k):
    chroma = get_chroma()

    result = chroma.similarity_search(
        query=job_description,
        k=k
    )

    shortlisted = []

    for r in result:
        shortlisted.append({
            "file": r.metadata["file_name"],
            "pages": r.metadata["pages"],
            "content": r.page_content
        })

    return shortlisted
