from fastapi import APIRouter
from app.api.routes import health,users,posts,communities,content,engagement,ai
api_router=APIRouter()
for r in [health.router,users.router,posts.router,communities.router,content.router,engagement.router,ai.router]: api_router.include_router(r)
