from fastapi import APIRouter,Depends,Query
from sqlalchemy import or_,select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import GoGuide,LearningContent,Event,RadioShow,RadioEpisode,CultureCast
router=APIRouter(tags=["Content"])
@router.get("/guides")
def guides(search:str|None=Query(None),db:Session=Depends(get_db)):
    q=select(GoGuide)
    if search:
        p=f"%{search}%";q=q.where(or_(GoGuide.title.ilike(p),GoGuide.description.ilike(p),GoGuide.category.ilike(p),GoGuide.keywords.ilike(p)))
    return db.scalars(q.order_by(GoGuide.title)).all()
@router.get("/learning")
def learning(db:Session=Depends(get_db)): return db.scalars(select(LearningContent).order_by(LearningContent.title)).all()
@router.get("/events")
def events(db:Session=Depends(get_db)): return db.scalars(select(Event).order_by(Event.event_date,Event.start_time)).all()
@router.get("/radio/episodes")
def radio(db:Session=Depends(get_db)):
    rows=db.execute(select(RadioEpisode,RadioShow).join(RadioShow,RadioEpisode.show_id==RadioShow.show_id).order_by(RadioEpisode.published_at.desc())).all()
    return [{"episode_id":e.episode_id,"show":s.title,"title":e.title,"description":e.description,"audio_url":e.audio_url,"thumbnail_url":e.thumbnail_url,"duration_seconds":e.duration_seconds,"published_at":e.published_at} for e,s in rows]
@router.get("/culture-cast")
def culture(db:Session=Depends(get_db)): return db.scalars(select(CultureCast).order_by(CultureCast.published_at.desc())).all()
