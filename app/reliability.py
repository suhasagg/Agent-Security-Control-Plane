def assess(r):
    # Reliability is treated as a security input: excessive delegation and unclear/high-impact plans add obligations.
    issues=[]
    if r.task.delegation_depth>4: issues.append("DELEGATION_DEPTH_EXCEEDED")
    if len(r.action.arguments)>30: issues.append("COMPLEX_ACTION_ARGUMENTS")
    if r.action.side_effect and not r.task.current_step.strip(): issues.append("MISSING_CURRENT_STEP")
    return issues
