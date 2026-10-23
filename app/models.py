
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from sqlalchemy.orm import relationship

from app.database import Base


class ManualVersion(Base):
    __tablename__ = "manual_versions"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    version_label = Column(String, nullable=False)
    file_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sections = relationship(
        "ManualSection",
        back_populates="manual",
        cascade="all, delete-orphan",
    )


class ManualSection(Base):
    __tablename__ = "manual_sections"

    id = Column(Integer, primary_key=True, index=True)
    manual_id = Column(
        Integer,
        ForeignKey("manual_versions.id"),
        nullable=False,
    )
    section_number = Column(String, nullable=False)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    page = Column(Integer, nullable=True)

    manual = relationship(
        "ManualVersion",
        back_populates="sections",
    )

    __table_args__ = (
        UniqueConstraint(
            "manual_id",
            "section_number",
            "title",
            name="uq_manual_section",
        ),
    )
