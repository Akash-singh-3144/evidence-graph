from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database.connection import Base

class InvestigationStep(Base):
    __tablename__ = "investigation_steps"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    investigation_id = Column(String, ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False)
    step_type = Column(String, nullable=False) # e.g. 'TOOL_CALL', 'PLAN'
    tool_name = Column(String)
    status = Column(String)
    input_ = Column("input", JSON)
    output = Column(JSON)
    error = Column(String)
    latency_ms = Column(Integer)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    investigation = relationship("Investigation", back_populates="steps")
