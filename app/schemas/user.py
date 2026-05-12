from pydantic import BaseModel, EmailStr
from typing import List, Optional
from enum import Enum


class AgeRange(str, Enum):
    teen = "under 18"
    young_adult = "18-24"
    adult = "25-34"
    mature = "35+"


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserUpdateProfile(BaseModel):
    gender: str
    age: AgeRange


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class AddressOut(BaseModel):
    id: int
    street: str
    city: str
    state: str
    zip_code: str
    model_config = {"from_attributes": True}


class CardBase(BaseModel):
    card_number: str
    ccv: str
    exp: str
    cardholder_name: str


class CardOut(BaseModel):
    id: int
    card_number: str
    exp: str
    ccv: str
    cardholder_name: str
    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    image_url: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[str] = None


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    image_url: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[str] = None

    # Nested lists
    addresses: List[AddressOut] = []
    cards: List[CardOut] = []

    model_config = {"from_attributes": True}
