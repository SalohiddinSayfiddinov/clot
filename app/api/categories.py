from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.category import Category
from app.schemas.category import CategoryBase, CategoryOut, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    query = db.query(Category)

    categories = query.all()

    return categories


@router.post("/create", response_model=CategoryOut)
def create_category(category_in: CategoryBase, db: Session = Depends(get_db)):
    new_category = Category(**category_in.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.patch("/{category_id}/update", response_model=CategoryOut)
def update_category(
    category_id: int, category_update: CategoryUpdate, db: Session = Depends(get_db)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    update_data = category_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete("/{category_id}/delete")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category.products:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category: It contains associated products. Delete products first.",
        )

    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}
