from sqlalchemy import Column, String, DateTime, Enum, JSON, Boolean
from sqlalchemy.orm import relationship
import enum
import uuid
from datetime import datetime
from app.database.connection import Base

class SourceType(str, enum.Enum):
    PDF = "pdf"
    WEB = "web"
    DATABASE = "database"

class Source(Base):
    __tablename__ = "sources"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(Enum(SourceType), nullable=False)
    name = Column(String)
    url = Column(String) # For web sources
    metadata_ = Column("metadata", JSON, default={})
    content_hash = Column(String, unique=True, index=True)
    indexed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    documents = relationship("Document", back_populates="source", cascade="all, delete-orphan")
    evidence = relationship("Evidence", back_populates="source")
