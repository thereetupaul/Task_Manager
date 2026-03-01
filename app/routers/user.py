from fastapi import Depends, FastAPI,Response,status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,utils


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hash the password - user.password
    hashed_password = utils.Hash(user.password)
    user.password = hashed_password
    
    #new_user = models.User(email = user.email, password=user.password)
    print(user.dict())
    new_user = models.User(**user.dict())  #unpacking the dictionary using **
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    #retrieve the new post from database

    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id ==id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"user with id: {id} does not exist!")
    
    return user