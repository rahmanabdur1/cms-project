from pydantic import BaseModel
from typing import Optional, List, Generic, TypeVar
from datetime import datetime

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    limit: int
    has_more: bool


# ─── Interaction ────────────────────────────────────────────────────────────

class InteractionBase(BaseModel):
    keyword: str
    type: str
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None


class InteractionCreate(InteractionBase):
    pass


class InteractionOut(InteractionBase):
    id: int
    content_id: int

    class Config:
        from_attributes = True


# ─── Category ───────────────────────────────────────────────────────────────

class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str


class CategoryOut(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# ─── Content ────────────────────────────────────────────────────────────────

class ContentBase(BaseModel):
    title: str
    body: str
    category_id: Optional[int] = None
    slug: Optional[str] = None


class ContentCreate(ContentBase):
    interactions: Optional[List[InteractionCreate]] = []


class ContentUpdate(ContentBase):
    interactions: Optional[List[InteractionCreate]] = []


class ContentOut(ContentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    interactions: List[InteractionOut] = []
    category: Optional[CategoryOut] = None

    class Config:
        from_attributes = True