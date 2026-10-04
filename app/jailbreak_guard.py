import re
# Defensive heuristic layer only; production should combine model/content classifiers and policy.
MARKERS=[
 r"jailbreak",r"ignore safety",r"without restrictions",r"developer mode",
 r"pretend (there are|you have) no rules",r"override .*guardrail",r"bypass .*filter"
]
def inspect(text):
    hits=[p for p in MARKERS if re.search(p,text.lower())]
    return min(50,len(hits)*15),hits
