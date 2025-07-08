from sqlalchemy import Column, String, DateTime
from .database import Base
from datetime import datetime

class Instance(Base):
    __tablename__ = "instances"

    instance_id = Column(String, primary_key=True, index=True)
    status = Column(String)
    version = Column(String)
    last_heartbeat = Column(DateTime, default=datetime.utcnow)
