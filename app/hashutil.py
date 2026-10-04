import hashlib,json
def action_hash(r):
    x={"tenant":r.principal.tenant_id,"user":r.principal.user_id,"agent":r.principal.agent_id,
       "task":r.task.original_task,"tool":r.action.tool_id,"operation":r.action.operation,
       "resource":r.action.resource,"arguments":r.action.arguments,"environment":r.action.environment,
       "classification":r.action.classification,"side_effect":r.action.side_effect}
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
