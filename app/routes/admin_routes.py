from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.audit import AuditLog
from app.models.user import User
from app.models.blog import Blog

from app.schemas.user_schema import UserResponse
from app.utils.dependencies import require_role
from app.services.audit_service import log_action

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/audit-logs", status_code=status.HTTP_200_OK)
def get_logs(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    admin=Depends(require_role(["admin"]))
):
    logs = (
        db.query(AuditLog)
        .order_by(AuditLog.timestamp.desc())
        .offset(skip)
        .limit(min(limit, 100))
        .all()
    )

    return {
        "success": True,
        "count": len(logs),
        "data": logs
    }
    
@router.get("/users", response_model=list[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    admin=Depends(require_role(["admin"]))
):
    users = (
        db.query(User)
        .offset(skip)
        .limit(min(limit, 100))
        .all()
    )

    return users

@router.delete("/blogs/{blog_id}", status_code=status.HTTP_200_OK)
def delete_any_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_role(["admin"]))
):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    db.delete(blog)
    db.commit()

    log_action(
        db,
        admin.id,
        "ADMIN_DELETE_BLOG",
        {"blog_id": blog_id}
    )

    return {
        "success": True,
        "message": "Blog deleted by admin"
    }