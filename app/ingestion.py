
import hashlib
from pathlib import Path

from sqlalchemy.orm import Session

from app.models import ManualSection, ManualVersion
from app.parser import parse_pdf, extract_sections


def calculate_file_hash(file_path: str) -> str:
    """Calculate a SHA-256 hash for a PDF file."""
    digest = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)

    return digest.hexdigest()


def ingest_manual(
    db: Session,
    file_path: str,
    version_label: str,
) -> dict:
    """Parse a manual and store its version and sections."""

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Manual not found: {path}")

    file_hash = calculate_file_hash(str(path))

    existing = (
        db.query(ManualVersion)
        .filter(ManualVersion.file_hash == file_hash)
        .first()
    )

    if existing:
        return {
            "manual_id": existing.id,
            "filename": existing.filename,
            "version_label": existing.version_label,
            "pages_processed": 0,
            "sections_found": len(existing.sections),
            "already_exists": True,
        }

    pages = parse_pdf(str(path))
    sections = extract_sections(pages)

    manual = ManualVersion(
        filename=path.name,
        version_label=version_label,
        file_hash=file_hash,
    )

    db.add(manual)
    db.flush()

    for section in sections:
        db.add(
            ManualSection(
                manual_id=manual.id,
                section_number=section["section_number"],
                title=section["title"],
                text=section["text"].strip(),
                page=section["page"],
            )
        )

    try:
        db.commit()
        db.refresh(manual)
    except Exception:
        db.rollback()
        raise

    return {
        "manual_id": manual.id,
        "filename": manual.filename,
        "version_label": manual.version_label,
        "pages_processed": len(pages),
        "sections_found": len(sections),
        "already_exists": False,
    }
