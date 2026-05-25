from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import User
from schemas import UserCreate, UserResponse
import models, uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE USER
@app.post("/users")
def create_user(user: UserCreate):
    db: Session = next(get_db())
    new_user = User(
        name=user.name,
        email=user.email,
        age=user.age
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message": "User Created Successfully",
        "data": new_user
    }

# GET ALL USERS
@app.get("/users")
def get_users():
    db: Session = next(get_db())
    users = db.query(User).all()
    return users

# GET SINGLE USER
@app.get("/users/{user_id}")
def get_single_user(user_id: int):
    db: Session = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )
    return user

# UPDATE USER
@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: UserCreate):
    db: Session = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )

    user.name = updated_user.name
    user.email = updated_user.email
    user.age = updated_user.age
    db.commit()
    db.refresh(user)
    return {
        "message": "User Updated Successfully",
        "data": user
    }

# DELETE USER
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db: Session = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )
    db.delete(user)
    db.commit()
    return {
        "message": "User Deleted Successfully"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000)