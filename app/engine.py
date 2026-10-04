from app.domain import SecurityDecision,Finding
from app.injection_guard import inspect as injection
from app.jailbreak_guard import inspect as jailbreak
from app.task_alignment import check as alignment
from app.memory_guard import inspect as memory
from app.permission import check as permissions
from app.risk import score
from app.reliability import assess
from app.hashutil import action_hash
from app.config import settings
def decide(r):
    findings=[];reasons=[]
    inj,inj_hits=injection(r.action.external_content)
    findings.append(Finding(control="prompt_injection",severity="HIGH" if inj else "INFO",passed=inj==0,reason=f"signals={len(inj_hits)}"))
    jb,jb_hits=jailbreak(r.task.original_task+" "+r.task.current_step)
    findings.append(Finding(control="jailbreak",severity="HIGH" if jb else "INFO",passed=jb==0,reason=f"signals={len(jb_hits)}"))
    aligned,why=alignment(r.task,r.action)
    findings.append(Finding(control="task_alignment",severity="HIGH" if not aligned else "INFO",passed=aligned,reason=why))
    mem=memory(r.action.memory_context)
    findings.append(Finding(control="memory_non_authority",severity="MEDIUM" if mem else "INFO",passed=True,reason="memory never grants authority; suspicious entries="+str(mem)))
    user,agent,cls=permissions(r)
    findings += [
      Finding(control="user_authority",severity="CRITICAL",passed=user,reason="user authority checked"),
      Finding(control="agent_authority",severity="CRITICAL",passed=agent,reason="agent authority checked"),
      Finding(control="classification",severity="HIGH",passed=cls,reason="classification clearance checked")]
    rel=assess(r)
    findings.append(Finding(control="reliability_constraints",severity="HIGH" if rel else "INFO",passed=not rel,reason=",".join(rel) if rel else "bounded"))
    rs,rr=score(r,inj,jb,aligned);reasons+=rr+rel
    if not user: reasons.append("USER_DENIED")
    if not agent: reasons.append("AGENT_DENIED")
    if not cls: reasons.append("CLASSIFICATION_DENIED")
    hard_deny=not user or not agent or not cls or r.task.delegation_depth>settings.max_delegation_depth
    if hard_deny: decision="DENY"
    elif inj>=30 and r.action.side_effect: decision="DENY";reasons.append("UNTRUSTED_INJECTION_BLOCK")
    elif not aligned and r.action.side_effect: decision="DENY"
    elif rs>=60 or (rs>=40 and r.action.environment=="production"): decision="APPROVAL";reasons.append("HUMAN_APPROVAL_REQUIRED")
    elif rs>=35 and not r.action.side_effect: decision="CLARIFY";reasons.append("CLARIFICATION_REQUIRED")
    else: decision="ALLOW"
    return SecurityDecision(decision=decision,risk_score=rs,findings=findings,reason_codes=sorted(set(reasons)),action_hash=action_hash(r),policy_version=settings.policy_version)
