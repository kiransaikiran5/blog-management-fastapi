from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException
from app.models.blog import Blog
from app.services.audit_service import log_action


# ➕ CREATE BLOG
def create_blog(db: Session, data, user):
    try:
        blog = Blog(
            title=data.title.strip(),
            content=data.content.strip(),
            status=data.status.lower(),
            author_id=user.id
        )

        db.add(blog)
        db.commit()
        db.refresh(blog)

        log_action(
            db,
            user.id,
            "CREATE_BLOG",
            {"blog_id": blog.id, "title": blog.title}
        )

        return blog

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create blog")


# 📄 GET SINGLE BLOG
def get_blog(db: Session, blog_id: int):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog


# ✏️ UPDATE BLOG
def update_blog(db: Session, blog_id: int, data, user):
    try:
        blog = get_blog(db, blog_id)

        # 🔐 RBAC
        if blog.author_id != user.id:
            raise HTTPException(status_code=403, detail="Forbidden")

        blog.title = data.title.strip()
        blog.content = data.content.strip()
        blog.status = data.status.lower()

        db.commit()
        db.refresh(blog)

        log_action(
            db,
            user.id,
            "UPDATE_BLOG",
            {"blog_id": blog.id}
        )

        return blog

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update blog")


# ❌ DELETE BLOG
def delete_blog(db: Session, blog_id: int, user):
    try:
        blog = get_blog(db, blog_id)

        # 🔐 RBAC (Admin OR Owner)
        if blog.author_id != user.id and user.role != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")

        db.delete(blog)
        db.commit()

        log_action(
            db,
            user.id,
            "DELETE_BLOG",
            {"blog_id": blog_id}
        )

        return {"message": "Blog deleted successfully"}

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete blog")


# 📄 GET BLOGS (Pagination + Search + Filter + Sorting)
def get_blogs(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: str = None,
    status: str = None,
    author_id: int = None,
    sort_by: str = "created_at",
    order: str = "desc"
):
    query = db.query(Blog)

    # 🔍 SEARCH
    if search:
        query = query.filter(
            or_(
                Blog.title.ilike(f"%{search}%"),
                Blog.content.ilike(f"%{search}%")
            )
        )

    # 🎯 FILTER
    if status:
        query = query.filter(Blog.status == status.lower())

    if author_id:
        query = query.filter(Blog.author_id == author_id)

    # 🔽 SAFE SORTING
    allowed_sort_fields = {
        "title": Blog.title,
        "created_at": Blog.created_at
    }

    sort_column = allowed_sort_fields.get(sort_by, Blog.created_at)

    if order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # 📄 PAGINATION LIMIT CONTROL
    limit = min(limit, 100)

    return query.offset(skip).limit(limit).all()