from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings
app=FastAPI(title=settings.app_name,version="0.1.0",description="Mastek Sphere Phase 1 backend API")
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origin_list,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.get("/")
def root(): return {"name":settings.app_name,"docs":"/docs","health":f"{settings.api_v1_prefix}/health"}
app.include_router(api_router,prefix=settings.api_v1_prefix)
