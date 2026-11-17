import os
os.environ.setdefault("DB_PASSWORD", "")
from app.main import app
routes=sorted({r.path for r in app.routes})
expected=["/api/v1/health","/api/v1/users","/api/v1/posts","/api/v1/communities","/api/v1/guides","/api/v1/events","/api/v1/radio/episodes","/api/v1/culture-cast","/api/v1/ai/chat"]
missing=[x for x in expected if x not in routes]
assert not missing, f"Missing routes: {missing}"
print(f"Route smoke test OK: {len(routes)} routes")
