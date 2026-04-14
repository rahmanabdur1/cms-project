from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Content, Interaction
from schemas import ContentCreate, ContentOut, ContentUpdate
from typing import List, Optional
import re

router = APIRouter(prefix="/contents", tags=["Contents"])


# ─── Helpers ────────────────────────────────────────────────────────────────

def generate_slug(title: str) -> str:
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug.strip("-")


def unique_slug(db: Session, base_slug: str, exclude_id: int = None) -> str:
    slug = base_slug
    counter = 1
    while True:
        query = db.query(Content).filter(Content.slug == slug)
        if exclude_id:
            query = query.filter(Content.id != exclude_id)
        if not query.first():
            return slug
        slug = f"{base_slug}-{counter}"
        counter += 1


# ─── Routes ─────────────────────────────────────────────────────────────────

@router.get("/count")
def get_contents_count(
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Content)
    if search:
        query = query.filter(Content.title.ilike(f"%{search}%"))
    if category_id:
        query = query.filter(Content.category_id == category_id)
    return {"count": query.count()}


@router.get("/slug/{slug}", response_model=ContentOut)
def get_content_by_slug(slug: str, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.slug == slug).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.get("/", response_model=List[ContentOut])
def get_contents(
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Content)
    if search:
        query = query.filter(Content.title.ilike(f"%{search}%"))
    if category_id:
        query = query.filter(Content.category_id == category_id)
    offset = (page - 1) * limit
    return (
        query.order_by(Content.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get("/{id}", response_model=ContentOut)
def get_content(id: int, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.id == id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.post("/", response_model=ContentOut)
def create_content(data: ContentCreate, db: Session = Depends(get_db)):
    base_slug = data.slug or generate_slug(data.title)
    slug = unique_slug(db, base_slug)

    content = Content(
        title=data.title,
        body=data.body,
        category_id=data.category_id,
        slug=slug,
    )
    db.add(content)
    db.commit()
    db.refresh(content)

    for item in data.interactions or []:
        db.add(Interaction(content_id=content.id, **item.dict()))
    db.commit()
    db.refresh(content)
    return content


@router.put("/{id}", response_model=ContentOut)
def update_content(id: int, data: ContentUpdate, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.id == id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Not found")

    base_slug = data.slug or generate_slug(data.title)
    content.title = data.title
    content.body = data.body
    content.category_id = data.category_id
    content.slug = unique_slug(db, base_slug, exclude_id=id)

    db.query(Interaction).filter(Interaction.content_id == id).delete()
    for item in data.interactions or []:
        db.add(Interaction(content_id=id, **item.dict()))

    db.commit()
    db.refresh(content)
    return content


@router.delete("/{id}")
def delete_content(id: int, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.id == id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(content)
    db.commit()
    return {"message": "Deleted"}