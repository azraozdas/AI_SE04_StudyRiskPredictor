"""
PDF utilities — deferred (no Streamlit upload UI in current MVP).

Provides text extraction and metadata reading for future course-material uploads.
Requires: pypdf (listed in requirements.txt for future use)

The pdfs table in Supabase is created by init_db(); files would live under Uploads/.
"""

import os
from pathlib import Path

# pypdf is an optional dependency — functions degrade gracefully if missing.
try:
    from pypdf import PdfReader
    _PYPDF_AVAILABLE = True
except ImportError:
    _PYPDF_AVAILABLE = False

UPLOADS_DIR = Path(__file__).parents[2] / "Uploads"


def extract_text(filepath: str) -> str:
    """Return all text extracted from a PDF file.

    Returns an empty string if pypdf is not installed or the file is unreadable.
    """
    if not _PYPDF_AVAILABLE:
        return ""
    try:
        reader = PdfReader(filepath)
        return "\n".join(
            page.extract_text() or "" for page in reader.pages
        ).strip()
    except Exception:
        return ""


def extract_metadata(filepath: str) -> dict:
    """Return basic PDF metadata: title, author, page_count.

    Returns a dict with None values if pypdf is unavailable or the file errors.
    """
    result = {"title": None, "author": None, "page_count": None}
    if not _PYPDF_AVAILABLE:
        return result
    try:
        reader = PdfReader(filepath)
        info = reader.metadata or {}
        result["title"]      = info.get("/Title")  or info.get("title")
        result["author"]     = info.get("/Author") or info.get("author")
        result["page_count"] = len(reader.pages)
    except Exception:
        pass
    return result


def save_upload(uploaded_file, user_id: int, course_id: int | None = None) -> str:
    """Save a Streamlit UploadedFile to Uploads/{user_id}/ and return the saved path.

    Does not write a DB record — call db.record_pdf() separately so the two
    operations can be transactional from the caller's perspective.
    """
    dest_dir = UPLOADS_DIR / str(user_id)
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest_path = dest_dir / uploaded_file.name
    # Avoid collisions with a counter suffix
    counter = 1
    while dest_path.exists():
        stem, suffix = os.path.splitext(uploaded_file.name)
        dest_path = dest_dir / f"{stem}_{counter}{suffix}"
        counter += 1

    with open(dest_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(dest_path)
