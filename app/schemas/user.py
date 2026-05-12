from pydantic import BaseModel, EmailStr
from typing import Optional
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


class UserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str

    model_config = {"from_attributes": True}


class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class AddressOut(AddressBase):
    id: int

    model_config = {"from_attributes": True}


class CardBase(BaseModel):
    card_number: str
    ccv: str
    exp: str
    cardholder_name: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    image_url: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[str] = None
