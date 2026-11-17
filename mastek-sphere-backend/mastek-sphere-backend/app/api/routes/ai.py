from fastapi import APIRouter
from pydantic import BaseModel
router=APIRouter(prefix="/ai",tags=["AI Agent"])
class ChatRequest(BaseModel): message:str
@router.post("/chat")
def chat(body:ChatRequest):
    return {"status":"coming_soon","message":"Mastek Sphere AI Agent integration is planned as an enhancement.","query":body.message}
