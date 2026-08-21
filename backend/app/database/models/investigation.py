from sqlalchemy import Column, String, DateTime, Enum, JSON, Float
from sqlalchemy.orm import relationship
import enum
import uuid
from datetime import datetime
from app.database.connection import Base

class InvestigationStatus(str, enum.Enum):
    INIT = "INIT"
    QUERY_ANALYSIS = "QUERY_ANALYSIS"
    PLANNING = "PLANNING"
    RETRIEVAL = "RETRIEVAL"
    EVIDENCE_NORMALIZATION = "EVIDENCE_NORMALIZATION"
    EVIDENCE_RANKING = "EVIDENCE_RANKING"
    CROSS_VERIFICATION = "CROSS_VERIFICATION"
    CONFLICT_DETECTION = "CONFLICT_DETECTION"
    EVIDENCE_GRAPH = "EVIDENCE_GRAPH"
    CONFIDENCE_SCORING = "CONFIDENCE_SCORING"
    SYNTHESIS = "SYNTHESIS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    WAITING_FOR_INPUT = "WAITING_FOR_INPUT"

class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    query = Column(String, nullable=False)
    plan = Column(JSON, default=[])
    status = Column(Enum(InvestigationStatus), default=InvestigationStatus.INIT)
    final_answer = Column(String)
    confidence_score = Column(Float)
    graph_data = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    steps = relationship("InvestigationStep", back_populates="investigation", cascade="all, delete-orphan")
    evidence = relationship("Evidence", back_populates="investigation", cascade="all, delete-orphan")
