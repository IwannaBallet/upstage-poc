from sqlalchemy import Column, Integer, Float, String, DateTime, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class VocLog(Base):
    __tablename__ = "voc_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    equipment_id = Column(String, index=True)
    temp = Column(Float)
    vibration = Column(Float)
    pressure = Column(Float)
    failure_type = Column(Integer)  # 0: Normal, 1: Failure
    solar_analysis = Column(JSON, nullable=True) # JSONB in Postgres
