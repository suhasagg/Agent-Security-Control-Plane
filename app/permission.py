def check(r):
    p,a=r.principal,r.action
    user=("admin" in p.user_roles or "agent.user" in p.user_roles or a.operation in p.user_roles)
    agent=("agent.admin" in p.agent_roles or "agent.execute" in p.agent_roles or a.tool_id in p.agent_roles)
    clearance=3 if "restricted.reader" in p.user_roles else 2 if "confidential.reader" in p.user_roles else 1
    cls={"PUBLIC":0,"INTERNAL":1,"CONFIDENTIAL":2,"RESTRICTED":3}[a.classification] <= clearance
    return user,agent,cls
