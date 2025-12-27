from config import get_chroma
from models.shortlist import generate_llm_response

chroma = get_chroma()

def retrieve_resumes(job_description: str, k: int = 3):
    results = chroma.similarity_search(job_description, k=k)

    return [
        {
            "file": r.metadata["file_name"],
            "pages": r.metadata["pages"],
            "text": r.page_content
        }
        for r in results
    ]


def evaluate_resume(job_description: str, resume: str):
    return generate_llm_response(job_description, resume)
