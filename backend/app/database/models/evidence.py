from sqlalchemy import Column, String, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database.connection import Base

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    investigation_id = Column(String, ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(String, ForeignKey("sources.id"), nullable=True) # Maybe internal logic etc
    normalized_json = Column(JSON, nullable=False)
    role = Column(String) # SUPPORTING, CONTRADICTING
    created_at = Column(DateTime, default=datetime.utcnow)

    investigation = relationship("Investigation", back_populates="evidence")
    source = relationship("Source", back_populates="evidence")
    
    # relationships where this evidence is the 'from' or 'to'
    related_to = relationship("EvidenceRelationship", foreign_keys="[EvidenceRelationship.from_evidence_id]", back_populates="from_evidence")
    related_from = relationship("EvidenceRelationship", foreign_keys="[EvidenceRelationship.to_evidence_id]", back_populates="to_evidence")
