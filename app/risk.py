def score(r,injection,jailbreak,aligned):
    a=r.action;s=injection+jailbreak;reasons=[]
    if injection: reasons.append("PROMPT_INJECTION_SIGNAL")
    if jailbreak: reasons.append("JAILBREAK_SIGNAL")
    if not aligned: s+=35;reasons.append("TASK_MISALIGNMENT")
    if a.environment=="production" and a.side_effect: s+=25;reasons.append("PRODUCTION_SIDE_EFFECT")
    if a.side_effect: s+=15;reasons.append("SIDE_EFFECT")
    if any(x in a.operation.lower() for x in ["delete","drop","destroy","terminate","transfer","purge"]):
        s+=25;reasons.append("HIGH_IMPACT_OPERATION")
    if a.classification=="CONFIDENTIAL": s+=10;reasons.append("CONFIDENTIAL")
    if a.classification=="RESTRICTED": s+=20;reasons.append("RESTRICTED")
    s=min(100,s)
    return s,reasons
