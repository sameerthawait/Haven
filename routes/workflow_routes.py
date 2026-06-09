from fastapi import APIRouter, Body
from typing import Any, Dict

router = APIRouter()


@router.post("/api/workflows/plan")
def plan_workflow(prompt: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """Return a proposed multi-step workflow based on a short prompt.

    MVP: returns a deterministic stub plan. Integrate agent generation later.
    """
    task = prompt.get("task") or "general"
    plan = [
        {"step": 1, "action": f"Draft content for '{task}'", "preview": "(draft text...)"},
        {"step": 2, "action": "Prepare calendar invite", "preview": "(invite preview)"},
        {"step": 3, "action": "Send follow-up email", "preview": "(email preview)"},
    ]
    return {"task": task, "plan": plan}


@router.post("/api/workflows/execute")
def execute_workflow(plan_id: str = Body(None), approved: bool = Body(False)) -> Dict[str, Any]:
    """Execute an approved workflow. Currently a safe stub that returns simulated results."""
    if not approved:
        return {"status": "pending_approval", "message": "Workflow execution requires approval"}
    # Simulate execution result
    return {"status": "executed", "results": [{"step": 1, "result": "draft_saved"}, {"step": 2, "result": "invite_created"}, {"step": 3, "result": "email_queued"}]}
