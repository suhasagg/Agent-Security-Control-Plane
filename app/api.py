from fastapi import APIRouter,Depends
from app.security import auth
from app.domain import SecurityRequest
from app.engine import decide
from app.store import persist
router=APIRouter(prefix="/v1",dependencies=[Depends(auth)])
@router.post("/security/evaluate")
async def evaluate(r:SecurityRequest):
    d=decide(r);d.approval_id=await persist(r,d);return d
