from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.orm import relationship
import uuid
from app.database.connection import Base

class EvidenceRelationshipType(str):
    SUPPORTS = "SUPPORTS"
    CONTRADICTS = "CONTRADICTS"
    CAUSES = "CAUSES"
    VERIFIES = "VERIFIES"
    DERIVED_FROM = "DERIVED_FROM"
    RELATED_TO = "RELATED_TO"

class EvidenceRelationship(Base):
    __tablename__ = "evidence_relationships"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    investigation_id = Column(String, ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False)
    from_evidence_id = Column(String, ForeignKey("evidence.id", ondelete="CASCADE"), nullable=False)
    to_evidence_id = Column(String, ForeignKey("evidence.id", ondelete="CASCADE"), nullable=False)
    relationship_type = Column(String, nullable=False) # EvidenceRelationshipType
    confidence = Column(Float)

    from_evidence = relationship("Evidence", foreign_keys=[from_evidence_id], back_populates="related_to")
    to_evidence = relationship("Evidence", foreign_keys=[to_evidence_id], back_populates="related_from")
