
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ManualVersionResponse(BaseModel):
    id: int
    filename: str
    version_label: str
    file_hash: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ManualSectionResponse(BaseModel):
    id: int
    manual_id: int
    section_number: str
    title: str
    text: str
    page: int | None = None

    model_config = ConfigDict(from_attributes=True)


class SectionSelection(BaseModel):
    section_number: str
    title: str
    text: str


class StalenessResult(BaseModel):
    section_number: str
    title: str
    status: str


class IngestResponse(BaseModel):
    message: str
    manual_id: int
    filename: str
    version_label: str
    pages_processed: int
    sections_found: int
