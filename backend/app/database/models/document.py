from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database.connection import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String, ForeignKey("sources.id"), nullable=False)
    file_name = Column(String, nullable=False)
    page_count = Column(Integer)
    content_hash = Column(String, unique=True, index=True)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    source = relationship("Source", back_populates="documents")
