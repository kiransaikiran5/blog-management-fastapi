from fastapi import FastAPI
from app.database import Base, engine

from app.routes import (
    auth_routes,
    blog_routes,
    comment_routes,
    admin_routes
)

# ✅ Create tables
Base.metadata.create_all(bind=engine)

# ✅ App instance
app = FastAPI(
    title="Blog Management API",
    description="Secure Blog API with JWT, RBAC, Comments, Audit Logs",
    version="1.0.0"
)

# ✅ Include routers (NO prefix if already defined inside route files)
app.include_router(auth_routes.router)
app.include_router(blog_routes.router)
app.include_router(comment_routes.router)
app.include_router(admin_routes.router)