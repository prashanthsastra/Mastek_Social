from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Post, User, PostLike, Comment
from app.schemas.common import PostCreate, CommentCreate, JoinRequest
router=APIRouter(prefix="/posts",tags=["Posts"])
def get_post_payload(db,p):
    u=db.get(User,p.user_id)
    likes=db.scalar(select(func.count()).select_from(PostLike).where(PostLike.post_id==p.post_id)) or 0
    comments=db.scalar(select(func.count()).select_from(Comment).where(Comment.post_id==p.post_id)) or 0
    return {"post_id":p.post_id,"user":{"user_id":u.user_id,"display_name":u.display_name,"job_title":u.job_title,"profile_image_url":u.profile_image_url},"content":p.content,"post_type":p.post_type,"media_url":p.media_url,"likes_count":likes,"comments_count":comments,"created_at":p.created_at,"updated_at":p.updated_at}
@router.get("")
def list_posts(db:Session=Depends(get_db)):
    return [get_post_payload(db,p) for p in db.scalars(select(Post).order_by(Post.created_at.desc())).all()]
@router.get("/{post_id}")
def get_post(post_id:UUID,db:Session=Depends(get_db)):
    p=db.get(Post,post_id)
    if not p: raise HTTPException(404,"Post not found")
    return get_post_payload(db,p)
@router.post("",status_code=201)
def create_post(body:PostCreate,db:Session=Depends(get_db)):
    if not db.get(User,body.user_id): raise HTTPException(404,"User not found")
    allowed={"TEXT","IMAGE","VIDEO","ARTICLE","POLL"}
    if body.post_type not in allowed: raise HTTPException(400,"Invalid post_type")
    p=Post(**body.model_dump()); db.add(p); db.commit(); db.refresh(p); return get_post_payload(db,p)
@router.delete("/{post_id}",status_code=204)
def delete_post(post_id:UUID,db:Session=Depends(get_db)):
    p=db.get(Post,post_id)
    if not p: raise HTTPException(404,"Post not found")
    db.delete(p); db.commit(); return Response(status_code=204)
@router.post("/{post_id}/like")
def like(post_id:UUID,body:JoinRequest,db:Session=Depends(get_db)):
    if not db.get(Post,post_id): raise HTTPException(404,"Post not found")
    if not db.get(User,body.user_id): raise HTTPException(404,"User not found")
    existing=db.get(PostLike,{"post_id":post_id,"user_id":body.user_id})
    if not existing: db.add(PostLike(post_id=post_id,user_id=body.user_id)); db.commit()
    return {"liked":True}
@router.delete("/{post_id}/like")
def unlike(post_id:UUID,user_id:UUID,db:Session=Depends(get_db)):
    x=db.get(PostLike,{"post_id":post_id,"user_id":user_id})
    if x: db.delete(x); db.commit()
    return {"liked":False}
@router.get("/{post_id}/comments")
def comments(post_id:UUID,db:Session=Depends(get_db)):
    rows=db.execute(select(Comment,User).join(User,User.user_id==Comment.user_id).where(Comment.post_id==post_id).order_by(Comment.created_at)).all()
    return [{"comment_id":c.comment_id,"user":{"user_id":u.user_id,"display_name":u.display_name},"comment_text":c.comment_text,"created_at":c.created_at} for c,u in rows]
@router.post("/{post_id}/comments",status_code=201)
def add_comment(post_id:UUID,body:CommentCreate,db:Session=Depends(get_db)):
    if not db.get(Post,post_id): raise HTTPException(404,"Post not found")
    c=Comment(post_id=post_id,user_id=body.user_id,comment_text=body.comment_text);db.add(c);db.commit();db.refresh(c);return c
