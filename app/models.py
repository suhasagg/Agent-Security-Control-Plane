import uuid
from datetime import datetime
from sqlalchemy import String,Integer,DateTime,Text
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.sql import func
from app.db import Base
def uid(): return uuid.uuid4()
class DecisionRecord(Base):
    __tablename__="security_decisions"
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id:Mapped[str]=mapped_column(String(128),index=True)
    user_id:Mapped[str]=mapped_column(String(256))
    agent_id:Mapped[str]=mapped_column(String(256),index=True)
    action_hash:Mapped[str]=mapped_column(String(64),index=True)
    decision:Mapped[str]=mapped_column(String(32))
    risk_score:Mapped[int]=mapped_column(Integer)
    reasons:Mapped[list]=mapped_column(JSONB)
    findings:Mapped[list]=mapped_column(JSONB)
    policy_version:Mapped[str]=mapped_column(String(64))
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
class Approval(Base):
    __tablename__="approvals"
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id:Mapped[str]=mapped_column(String(128),index=True)
    action_hash:Mapped[str]=mapped_column(String(64),index=True)
    status:Mapped[str]=mapped_column(String(32),default="PENDING")
    requested_by:Mapped[str]=mapped_column(String(256))
    approved_by:Mapped[str|None]=mapped_column(String(256),nullable=True)
    reason:Mapped[str|None]=mapped_column(Text,nullable=True)
    expires_at:Mapped[datetime]=mapped_column(DateTime(timezone=True))
class Audit(Base):
    __tablename__="audit"
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uid)
    tenant_id:Mapped[str]=mapped_column(String(128),index=True)
    event_type:Mapped[str]=mapped_column(String(128))
    actor:Mapped[str]=mapped_column(String(256))
    data:Mapped[dict]=mapped_column(JSONB)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
