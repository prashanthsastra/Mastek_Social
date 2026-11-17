from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import func,select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Community,CommunityMember
from app.schemas.common import JoinRequest
router=APIRouter(prefix="/communities",tags=["Communities"])
@router.get("")
def all(db:Session=Depends(get_db)):
    rows=db.execute(select(Community,func.count(CommunityMember.user_id)).outerjoin(CommunityMember).group_by(Community.community_id).order_by(Community.community_name)).all()
    return [{"community_id":c.community_id,"name":c.community_name,"description":c.description,"category":c.category,"image_url":c.image_url,"member_count":n} for c,n in rows]
@router.get("/{community_id}")
def one(community_id:UUID,db:Session=Depends(get_db)):
    c=db.get(Community,community_id)
    if not c: raise HTTPException(404,"Community not found")
    n=db.scalar(select(func.count()).select_from(CommunityMember).where(CommunityMember.community_id==community_id)) or 0
    return {"community_id":c.community_id,"name":c.community_name,"description":c.description,"category":c.category,"image_url":c.image_url,"member_count":n}
@router.post("/{community_id}/join")
def join(community_id:UUID,body:JoinRequest,db:Session=Depends(get_db)):
    if not db.get(Community,community_id): raise HTTPException(404,"Community not found")
    key={"community_id":community_id,"user_id":body.user_id}; x=db.get(CommunityMember,key)
    if not x: db.add(CommunityMember(**key,member_role="MEMBER"));db.commit()
    return {"joined":True}
@router.delete("/{community_id}/join")
def leave(community_id:UUID,user_id:UUID,db:Session=Depends(get_db)):
    x=db.get(CommunityMember,{"community_id":community_id,"user_id":user_id})
    if x and x.member_role!="OWNER": db.delete(x);db.commit()
    return {"joined":False}
