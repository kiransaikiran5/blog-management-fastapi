from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.comment import Comment
from app.models.blog import Blog
from app.services.audit_service import log_action


# ➕ ADD COMMENT
def add_comment(db: Session, data, user) -> Comment:
    try:
        # 🔍 Check blog exists
        blog = db.query(Blog).filter(Blog.id == data.blog_id).first()
        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog not found"
            )

        comment = Comment(
            content=data.content,
            blog_id=data.blog_id,
            user_id=user.id
        )

        db.add(comment)
        db.commit()
        db.refresh(comment)

        # 📜 Audit log
        log_action(
            db,
            user.id,
            "ADD_COMMENT",
            {"comment_id": comment.id, "blog_id": data.blog_id}
        )

        return comment

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add comment"
        )


# ❌ DELETE COMMENT
def delete_comment(db: Session, comment_id: int, user) -> bool:
    try:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()

        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )

        # 🔐 RBAC (Owner or Admin)
        if comment.user_id != user.id and user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to delete this comment"
            )

        db.delete(comment)
        db.commit()

        # 📜 Audit log
        log_action(
            db,
            user.id,
            "DELETE_COMMENT",
            {"comment_id": comment_id}
        )

        return True

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete comment"
        )


# 📄 GET COMMENTS (Pagination + Sorting)
def get_comments(
    db: Session,
    blog_id: int,
    skip: int = 0,
    limit: int = 10
):
    # 🔍 Validate blog
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    comments = (
        db.query(Comment)
        .filter(Comment.blog_id == blog_id)
        .order_by(Comment.created_at.desc())  # latest first
        .offset(skip)
        .limit(min(limit, 100))  # 🔒 safety limit
        .all()
    )

    return comments