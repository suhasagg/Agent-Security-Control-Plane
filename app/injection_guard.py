import re
PATTERNS=[
 r"ignore (all|any|the|previous|prior) (instructions|rules|policy)",
 r"(system|developer) message",
 r"(bypass|disable|override) (security|guard|policy|approval)",
 r"(reveal|print|exfiltrate).*(secret|token|password|credential)",
 r"you are now .*admin",
 r"do not tell the user"
]
def inspect(items):
    findings=[];score=0
    for item in items:
        if item.trust=="trusted": continue
        text=item.content.lower()
        hits=[p for p in PATTERNS if re.search(p,text)]
        if hits:
            score+=min(40,15+5*len(hits))
            findings.append({"source":item.source,"patterns":hits})
    return min(score,60),findings
