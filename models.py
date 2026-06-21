from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime


class ProductVersion(Base):
    __tablename__ = "product_versions"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, nullable=False)

    version_number = Column(String(20), nullable=False)

    status = Column(String(20), default="Pending")

    created_at = Column(DateTime, default=datetime.utcnow)



class ChangeLog(Base):
    __tablename__ = "change_logs"

    id = Column(Integer, primary_key=True, index=True)

    version_id = Column(Integer, nullable=False)

    requirement_id = Column(Integer, nullable=False)

    field_name = Column(String(100), nullable=False)

    old_value = Column(String(255))

    new_value = Column(String(255))

    reason = Column(String(255))

    modified_by = Column(String(100))

    timestamp = Column(DateTime, default=datetime.utcnow)


from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)

    version_id = Column(Integer)

    status = Column(String(20))

    comments = Column(String(255))

    approved_by = Column(String(100))
    
    approved_at = Column(DateTime)