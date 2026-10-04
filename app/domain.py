from pydantic import BaseModel, Field
from typing import Literal, Any
Decision=Literal["ALLOW","DENY","APPROVAL","CLARIFY"]
class Principal(BaseModel):
    tenant_id:str
    user_id:str
    agent_id:str
    user_roles:list[str]=Field(default_factory=list)
    agent_roles:list[str]=Field(default_factory=list)
class TaskContext(BaseModel):
    original_task:str
    current_step:str
    allowed_capabilities:list[str]=Field(default_factory=list)
    delegation_depth:int=0
class ContentItem(BaseModel):
    source:str
    content:str
    trust:Literal["trusted","untrusted","unknown"]="unknown"
class ProposedAction(BaseModel):
    tool_id:str
    operation:str
    resource:str
    arguments:dict[str,Any]=Field(default_factory=dict)
    environment:Literal["dev","test","staging","production"]="dev"
    classification:Literal["PUBLIC","INTERNAL","CONFIDENTIAL","RESTRICTED"]="INTERNAL"
    side_effect:bool=False
    external_content:list[ContentItem]=Field(default_factory=list)
    memory_context:list[ContentItem]=Field(default_factory=list)
class SecurityRequest(BaseModel):
    principal:Principal
    task:TaskContext
    action:ProposedAction
class Finding(BaseModel):
    control:str
    severity:Literal["INFO","LOW","MEDIUM","HIGH","CRITICAL"]
    passed:bool
    reason:str
class SecurityDecision(BaseModel):
    decision:Decision
    risk_score:int
    findings:list[Finding]
    reason_codes:list[str]
    action_hash:str
    policy_version:str
    approval_id:str|None=None
