from sqlalchemy.orm import Session
from app.models.user import Address
from fastapi import HTTPException


def get_address_string(address_id: int, db: Session) -> str:
    addr = db.query(Address).filter(Address.id == address_id).first()
    if not addr:
        raise HTTPException(status_code=404, detail="Address not found")

    return f"{addr.street}, {addr.city}, {addr.state} {addr.zip_code}"
