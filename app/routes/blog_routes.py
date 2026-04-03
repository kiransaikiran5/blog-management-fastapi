from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.blog_schema import BlogCreate, BlogResponse
from app.services.blog_service import create_blog, get_blogs, get_blog, update_blog, delete_blog
from app.utils.dependencies import get_current_user, require_role

router = APIRouter(prefix="/blogs", tags=["Blogs"])

# -------------------
# CREATE BLOG
# -------------------
@router.post("/", response_model=BlogResponse)
def create_blog_api(
    data: BlogCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role(["author"]))
):
    blog = create_blog(db, data, user)
    return blog


# -------------------
# GET ALL BLOGS
# -------------------
@router.get("/", response_model=List[BlogResponse])
def get_all_blogs(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    status: Optional[str] = None,
    author_id: Optional[int] = None,
    sort_by: str = "created_at",
    order: str = "desc",
    db: Session = Depends(get_db)
):
    blogs = get_blogs(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        status=status,
        author_id=author_id,
        sort_by=sort_by,
        order=order
    )
    return blogs


# -------------------
# GET SINGLE BLOG
# -------------------
@router.get("/{blog_id}", response_model=BlogResponse)
def get_single_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


# -------------------
# UPDATE BLOG
# -------------------
@router.put("/{blog_id}", response_model=BlogResponse)
def update_blog_api(
    blog_id: int,
    data: BlogCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    result = update_blog(db, blog_id, data, user)

    if result == "forbidden":
        raise HTTPException(status_code=403, detail="Forbidden")

    if not result:
        raise HTTPException(status_code=404, detail="Blog not found")

    return result


# -------------------
# DELETE BLOG
# -------------------
@router.delete("/{blog_id}", status_code=200)
def delete_blog_api(
    blog_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    result = delete_blog(db, blog_id, user)

    if result == "forbidden":
        raise HTTPException(status_code=403, detail="Forbidden")

    if not result:
        raise HTTPException(status_code=404, detail="Blog not found")

    return {"msg": "Blog deleted successfully"}