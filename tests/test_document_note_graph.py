"""Tests for the document note graph and backlinks routes."""
import tempfile
import uuid
from types import SimpleNamespace

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from unittest.mock import MagicMock

from tests.helpers.import_state import clear_fake_database_modules

clear_fake_database_modules()

import core.database as cdb
import routes.document_routes as droutes
from core.database import Document
from core.database import Session as DbSession

_TMPDB = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_ENGINE = create_engine(
    f"sqlite:///{_TMPDB.name}",
    connect_args={"check_same_thread": False},
    poolclass=NullPool,
)
cdb.Base.metadata.create_all(_ENGINE)
_TS = sessionmaker(bind=_ENGINE, autoflush=False, autocommit=False)
droutes.SessionLocal = _TS


def _req():
    return SimpleNamespace(state=SimpleNamespace(current_user="tester"))


def _endpoint(method, path):
    router = droutes.setup_document_routes(MagicMock(), None)
    for r in router.routes:
        if getattr(r, "path", None) == path and method in getattr(r, "methods", set()):
            return r.endpoint
    raise RuntimeError(f"{method} {path} not found")


def _make_doc(title, content, archived=False, is_active=True, owner="tester"):
    sid = "s-" + uuid.uuid4().hex[:8]
    db = _TS()
    try:
        session = db.query(DbSession).filter(DbSession.id == sid).first()
        if not session:
            db.add(DbSession(id=sid, owner=owner, name="s", model="m", endpoint_url="http://x"))
        doc = Document(
            id=str(uuid.uuid4()), session_id=sid, title=title,
            language="markdown", current_content=content, version_count=1,
            is_active=is_active, owner=owner, archived=archived
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc.id
    finally:
        db.close()


async def test_get_documents_graph_empty():
    get_graph = _endpoint("GET", "/api/documents/graph")
    
    db = _TS()
    try:
        db.query(Document).delete()
        db.commit()
    finally:
        db.close()
        
    res = await get_graph(_req())
    assert res == {"nodes": [], "links": []}


async def test_get_documents_graph_with_links():
    get_graph = _endpoint("GET", "/api/documents/graph")
    
    doc_b_id = _make_doc("Document B", "Some text here.")
    doc_a_id = _make_doc("Document A", "Link to [[Document B]] and an invalid link [[Nonexistent]].")
    
    res = await get_graph(_req())
    nodes = {node["id"]: node for node in res["nodes"]}
    assert doc_a_id in nodes
    assert doc_b_id in nodes
    assert nodes[doc_a_id]["title"] == "Document A"
    assert nodes[doc_b_id]["title"] == "Document B"
    
    assert len(res["links"]) == 1
    assert res["links"][0] == {"source": doc_a_id, "target": doc_b_id}


async def test_get_document_backlinks():
    get_backlinks = _endpoint("GET", "/api/document/{doc_id}/backlinks")
    
    doc_a_id = _make_doc("Document A", "No links.")
    doc_b_id = _make_doc("Document B", "I link to [[Document A]].")
    doc_c_id = _make_doc("Document C", "I also link to [[Document A]].")
    
    res = await get_backlinks(_req(), doc_a_id)
    assert len(res) == 2
    backlink_ids = [bl["id"] for bl in res]
    assert doc_b_id in backlink_ids
    assert doc_c_id in backlink_ids
    
    for bl in res:
        if bl["id"] == doc_b_id:
            assert bl["title"] == "Document B"
            assert bl["updated_at"] is not None


async def test_exclude_archived_and_inactive_documents():
    get_graph = _endpoint("GET", "/api/documents/graph")
    
    doc_active_id = _make_doc("Active Doc", "Normal content.", archived=False, is_active=True)
    doc_archived_id = _make_doc("Archived Doc", "Archived content.", archived=True, is_active=True)
    doc_inactive_id = _make_doc("Inactive Doc", "Inactive content.", archived=False, is_active=False)
    
    res = await get_graph(_req())
    nodes = [node["id"] for node in res["nodes"]]
    assert doc_active_id in nodes
    assert doc_archived_id not in nodes
    assert doc_inactive_id not in nodes
