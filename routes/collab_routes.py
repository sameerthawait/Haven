from fastapi import APIRouter, Body
from typing import Any, Dict
import uuid

router = APIRouter()


@router.post("/api/collab/session")
def create_collab_session(payload: Dict[str, Any] = Body(None)) -> Dict[str, Any]:
    """Create an ephemeral collaboration session token (MVP stub)."""
    sid = str(uuid.uuid4())
    return {"session_id": sid, "url": f"/collab/{sid}", "expires_in": 3600}


@router.get("/api/collab/presence/{session_id}")
def get_presence(session_id: str) -> Dict[str, Any]:
    """Return mock presence information for a session."""
    return {"session_id": session_id, "users": [{"id": "u1", "name": "You"}], "active": True}
