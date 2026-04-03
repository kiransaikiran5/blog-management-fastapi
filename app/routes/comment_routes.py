from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.comment_schema import CommentCreate, CommentResponse
from app.services.comment_service import (
    add_comment,
    delete_comment,
    get_comments
)
from app.utils.dependencies import get_current_user

# ✅ Add prefix + tags (IMPORTANT)
router = APIRouter(prefix="/comments", tags=["Comments"])


# ➕ Add Comment
@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def add_comment_api(
    data: CommentCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return add_comment(db, data, user)


# 📄 Get Comments by Blog (Pagination)
@router.get("/blog/{blog_id}", response_model=list[CommentResponse])
def get_comments_api(
    blog_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    comments = get_comments(db, blog_id, skip, limit)

    return comments

# ❌ Delete Comment
@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
def delete_comment_api(
    comment_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    delete_comment(db, comment_id, user)

    return {
        "success": True,
        "message": "Comment deleted successfully"
    }