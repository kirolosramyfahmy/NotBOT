from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class MissionStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    DETECTED = "DETECTED"
    CLEAN = "CLEAN"
    ERROR = "ERROR"

class Mission(Base):
    __tablename__ = "investigations"

    id = Column(Integer, primary_key=True, index=True)
    brand_name = Column(String, nullable=False)
    target_url = Column(String, nullable=False)
    status = Column(String, default=MissionStatus.PENDING)
    evidence_path = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
