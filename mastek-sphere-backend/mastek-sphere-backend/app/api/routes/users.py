from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import User, UserSkill, Skill
router=APIRouter(prefix="/users",tags=["Users"])
def serialize_user(db,u):
    skills=db.execute(select(Skill.skill_name,UserSkill.proficiency_level).join(UserSkill,Skill.skill_id==UserSkill.skill_id).where(UserSkill.user_id==u.user_id)).all()
    return {"user_id":u.user_id,"employee_id":u.employee_id,"display_name":u.display_name,"email":u.email,"job_title":u.job_title,"department":u.department,"location":u.location,"bio":u.bio,"profile_image_url":u.profile_image_url,"cover_image_url":u.cover_image_url,"skills":[{"name":x[0],"proficiency":x[1]} for x in skills]}
@router.get("")
def list_users(search:str|None=Query(None),db:Session=Depends(get_db)):
    q=select(User).where(User.user_status=="ACTIVE")
    if search:
        p=f"%{search}%"
        q=q.where(or_(User.display_name.ilike(p),User.job_title.ilike(p),User.department.ilike(p),User.location.ilike(p),User.user_id.in_(select(UserSkill.user_id).join(Skill).where(Skill.skill_name.ilike(p)))))
    return [serialize_user(db,u) for u in db.scalars(q.order_by(User.display_name)).all()]
@router.get("/{user_id}")
def get_user(user_id:UUID,db:Session=Depends(get_db)):
    u=db.get(User,user_id)
    if not u: raise HTTPException(404,"User not found")
    return serialize_user(db,u)
