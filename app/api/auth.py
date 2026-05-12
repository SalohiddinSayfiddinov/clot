from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdateProfile, UserLogin
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    # 1. Find user by email
    user = db.query(User).filter(User.email == user_in.email).first()

    # 2. Check if user exists and password is correct
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Create the token
    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
    }


@router.post("/signup", response_model=UserOut)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Check if email already exists
    user_exists = db.query(User).filter(User.email == user_in.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )

    # 2. Hash the password and create user object
    new_user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )

    # 3. Save to Postgres
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.patch("/complete-profile/{user_id}", response_model=UserOut)
def complete_profile(
    user_id: int, profile_data: UserUpdateProfile, db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.gender = profile_data.gender
    user.age = profile_data.age

    db.commit()
    db.refresh(user)
    return user
