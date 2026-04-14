from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Category
from schemas import CategoryCreate, CategoryOut, CategoryUpdate
from typing import List

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.get("/{id}", response_model=CategoryOut)
def get_category(id: int, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.id == id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat


@router.post("/", response_model=CategoryOut)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(**data.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{id}", response_model=CategoryOut)
def update_category(id: int, data: CategoryUpdate, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.id == id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    cat.name = data.name
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.id == id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(cat)
    db.commit()
    return {"message": "Deleted"}