from fastapi import APIRouter,Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Recognition,SavedItem,Notification,User
from app.schemas.common import RecognitionCreate,SaveCreate
router=APIRouter(tags=["Engagement"])
@router.get("/recognition")
def recognitions(db:Session=Depends(get_db)):
    rs=db.scalars(select(Recognition).order_by(Recognition.created_at.desc())).all(); out=[]
    for r in rs:
        s=db.get(User,r.sender_id);v=db.get(User,r.receiver_id);out.append({"recognition_id":r.recognition_id,"sender":s.display_name,"receiver":v.display_name,"recognition_type":r.recognition_type,"message":r.message,"created_at":r.created_at})
    return out
@router.post("/recognition",status_code=201)
def create_recognition(body:RecognitionCreate,db:Session=Depends(get_db)):
    r=Recognition(**body.model_dump());db.add(r);db.commit();db.refresh(r);return r
@router.get("/saved")
def saved(user_id:str,db:Session=Depends(get_db)): return db.scalars(select(SavedItem).where(SavedItem.user_id==user_id).order_by(SavedItem.created_at.desc())).all()
@router.post("/saved",status_code=201)
def save(body:SaveCreate,db:Session=Depends(get_db)):
    x=SavedItem(**body.model_dump());db.add(x)
    try: db.commit();db.refresh(x);return x
    except IntegrityError: db.rollback();return {"status":"already_saved"}
@router.get("/notifications")
def notifications(user_id:str,db:Session=Depends(get_db)): return db.scalars(select(Notification).where(Notification.user_id==user_id).order_by(Notification.created_at.desc())).all()
