# models/agent.py

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any
from models.agent_tools import retrieve_resumes, evaluate_resume
import os

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# --------- DEFINE STATE ---------
class AgentState(TypedDict):
    job_desc: str
    k: int
    resumes: List[Dict[str, Any]]
    final: List[Dict[str, Any]]


# --------- NODES ---------
def retrieve_node(state: AgentState):
    resumes = retrieve_resumes(state["job_desc"], state["k"])
    return {
        "resumes": resumes,
        "job_desc": state["job_desc"],
        "k": state["k"]
    }


def evaluate_node(state: AgentState):
    job_desc = state["job_desc"]
    evaluated = []

    for r in state["resumes"]:
        evaluation = evaluate_resume(job_desc, r["text"])
        evaluated.append({
            "file": r["file"],
            "pages": r["pages"],
            "summary": evaluation
        })

    return {"final": evaluated}


# --------- BUILD GRAPH ---------
graph = StateGraph(AgentState)

graph.add_node("retrieve", retrieve_node)
graph.add_node("evaluate", evaluate_node)

graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "evaluate")

agent_graph = graph.compile()


# --------- PUBLIC FUNCTION ---------
def agentic_shortlist(job_description: str, k: int):
    result = agent_graph.invoke({
        "job_desc": job_description,
        "k": k
    })

    return result["final"]
