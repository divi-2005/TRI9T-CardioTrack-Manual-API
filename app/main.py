
from pathlib import Path

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.ingestion import ingest_manual
from app.models import ManualSection, ManualVersion
from app.versioning import compare_sections


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CardioTrack Manual API")


# Home endpoint
@app.get("/")
def home():
    return {"message": "CardioTrack Manual API is running"}


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Upload and ingest a PDF manual
@app.post("/manuals/ingest")
def upload_manual(
    file: UploadFile = File(...),
    version_label: str = Form(...),
    db: Session = Depends(get_db),
):
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    upload_dir = Path("data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    safe_filename = Path(file.filename).name
    temp_path = upload_dir / safe_filename

    try:
        with temp_path.open("wb") as destination:
            while chunk := file.file.read(1024 * 1024):
                destination.write(chunk)

        result = ingest_manual(
            db=db,
            file_path=str(temp_path),
            version_label=version_label
        )

        return {
            "message": (
                "Manual already exists"
                if result["already_exists"]
                else "Manual ingested successfully"
            ),
            **result,
        }

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Manual ingestion failed: {error}"
        ) from error

    finally:
        file.file.close()
        if temp_path.exists():
            temp_path.unlink()


# List all uploaded manual versions
@app.get("/manuals")
def list_manuals(db: Session = Depends(get_db)):
    manuals = (
        db.query(ManualVersion)
        .order_by(ManualVersion.id)
        .all()
    )

    return [
        {
            "id": manual.id,
            "filename": manual.filename,
            "version_label": manual.version_label,
            "created_at": manual.created_at,
            "sections_count": len(manual.sections),
        }
        for manual in manuals
    ]


# Get sections belonging to a manual
@app.get("/manuals/{manual_id}/sections")
def get_manual_sections(
    manual_id: int,
    db: Session = Depends(get_db)
):
    manual = (
        db.query(ManualVersion)
        .filter(ManualVersion.id == manual_id)
        .first()
    )

    if manual is None:
        raise HTTPException(
            status_code=404,
            detail="Manual not found."
        )

    sections = (
        db.query(ManualSection)
        .filter(ManualSection.manual_id == manual_id)
        .order_by(ManualSection.id)
        .all()
    )

    return [
        {
            "section_number": section.section_number,
            "title": section.title,
            "text": section.text,
            "page": section.page,
        }
        for section in sections
    ]


# Compare two manual versions
@app.get("/manuals/compare/{old_id}/{new_id}")
def compare_manual_versions(
    old_id: int,
    new_id: int,
    db: Session = Depends(get_db),
):
    old_manual = (
        db.query(ManualVersion)
        .filter(ManualVersion.id == old_id)
        .first()
    )

    new_manual = (
        db.query(ManualVersion)
        .filter(ManualVersion.id == new_id)
        .first()
    )

    if old_manual is None:
        raise HTTPException(
            status_code=404,
            detail=f"Manual version {old_id} not found."
        )

    if new_manual is None:
        raise HTTPException(
            status_code=404,
            detail=f"Manual version {new_id} not found."
        )

    old_sections = [
        {
            "section_number": section.section_number,
            "title": section.title,
            "text": section.text,
        }
        for section in old_manual.sections
    ]

    new_sections = [
        {
            "section_number": section.section_number,
            "title": section.title,
            "text": section.text,
        }
        for section in new_manual.sections
    ]

    comparison = compare_sections(
        old_sections,
        new_sections
    )

    return {
        "old_version": old_manual.version_label,
        "new_version": new_manual.version_label,
        "summary": {
            "added": len(comparison["added"]),
            "removed": len(comparison["removed"]),
            "changed": len(comparison["changed"]),
            "unchanged": len(comparison["unchanged"]),
        },
        "details": comparison,
    }
