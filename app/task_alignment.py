TOKENS={"delete","drop","send","email","upload","download","query","read","write","deploy","restart","refund","transfer","create","update"}
def check(task,action):
    task_words=set(task.original_task.lower().replace("/"," ").split())
    op=action.operation.lower()
    cap_ok=(not task.allowed_capabilities) or action.tool_id in task.allowed_capabilities
    op_hint=op in task_words or any(t in task_words and t in op for t in TOKENS)
    if action.side_effect and not op_hint:
        return False,"side-effecting operation is not clearly aligned with the original task"
    if not cap_ok:
        return False,"tool is outside the task capability envelope"
    return True,"action is within declared task/capability envelope"
