from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User, Address, PaymentCard
from app.schemas.user import (
    UserOut,
    AddressOut,
    AddressBase,
    CardBase,
)  # Ensure these are in schemas
from app.core.security import get_current_user

router = APIRouter(prefix="/user", tags=["User Profile"])

# --- Profile Management ---


@router.get("/me", response_model=UserOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Returns the full user profile including nested addresses and cards.
    """
    return current_user


@router.patch("/update", response_model=UserOut)
def update_profile(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    image_url: Optional[str] = Form(None),  # Frontend sends the string URL here
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_user.first_name = first_name
    current_user.last_name = last_name
    current_user.email = email
    current_user.phone = phone
    current_user.image_url = image_url

    db.commit()
    db.refresh(current_user)
    return current_user


# --- Address CRUD ---


@router.get("/addresses", response_model=List[AddressOut])
def get_addresses(current_user: User = Depends(get_current_user)):
    return current_user.addresses


@router.post("/addresses", response_model=AddressOut)
def add_address(
    address: AddressBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_address = Address(**address.model_dump(), user_id=current_user.id)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address


@router.delete("/addresses/{address_id}")
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    addr = (
        db.query(Address)
        .filter(Address.id == address_id, Address.user_id == current_user.id)
        .first()
    )
    if not addr:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(addr)
    db.commit()
    return {"message": "Address deleted"}


# --- Payment Card CRUD ---


@router.get("/cards")
def get_cards(current_user: User = Depends(get_current_user)):
    return current_user.cards


@router.post("/cards")
def add_card(
    card: CardBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_card = PaymentCard(**card.model_dump(), user_id=current_user.id)
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card


@router.delete("/cards/{card_id}")
def delete_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    card = (
        db.query(PaymentCard)
        .filter(PaymentCard.id == card_id, PaymentCard.user_id == current_user.id)
        .first()
    )
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    db.delete(card)
    db.commit()
    return {"message": "Card deleted"}
