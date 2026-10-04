from datetime import datetime,timedelta,timezone
from app.db import Session
from app.models import DecisionRecord,Approval,Audit
from app.config import settings
async def persist(r,d):
    async with Session.begin() as s:
        s.add(DecisionRecord(tenant_id=r.principal.tenant_id,user_id=r.principal.user_id,agent_id=r.principal.agent_id,
          action_hash=d.action_hash,decision=d.decision,risk_score=d.risk_score,reasons=d.reason_codes,
          findings=[x.model_dump() for x in d.findings],policy_version=d.policy_version))
        aid=None
        if d.decision=="APPROVAL":
            a=Approval(tenant_id=r.principal.tenant_id,action_hash=d.action_hash,requested_by=r.principal.user_id,
              expires_at=datetime.now(timezone.utc)+timedelta(seconds=settings.approval_ttl_seconds))
            s.add(a);await s.flush();aid=str(a.id)
        s.add(Audit(tenant_id=r.principal.tenant_id,event_type="SECURITY_DECISION",actor=r.principal.agent_id,
          data={"action_hash":d.action_hash,"decision":d.decision,"risk":d.risk_score,"reasons":d.reason_codes}))
        return aid
