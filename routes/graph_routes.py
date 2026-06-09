from fastapi import APIRouter
from typing import Any, Dict

from src.rag_manager import RAGManager

router = APIRouter()
rag = RAGManager()


@router.get("/api/graph/concepts")
def get_concept_graph(limit: int = 50) -> Dict[str, Any]:
    """Return a lightweight concept graph for the UI.

    This is an MVP stub that samples top documents and builds a simple
    node/link structure. Replace with richer semantic clustering later.
    """
    if not rag.vector_rag.healthy:
        return {"nodes": [], "links": [], "message": "RAG unavailable"}

    # Simple heuristic: take top N documents from a generic query
    docs = rag.search("", k=min(10, limit))
    nodes = []
    links = []
    for i, d in enumerate(docs):
        nodes.append({"id": d.get("id", f"doc{i}"), "title": (d.get("metadata", {}).get("title") or d.get("document", "(no title)"))[:80], "lang": d.get("metadata", {}).get("language")})
        if i > 0:
            links.append({"source": nodes[0]["id"], "target": nodes[i]["id"], "weight": round(1.0 - float(d.get("distance", 0)), 2)})

    return {"nodes": nodes, "links": links}
