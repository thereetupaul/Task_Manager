from fastapi import Depends, FastAPI,Response,status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,utils,oauth2


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


@router.get("/me", response_model=schemas.UserOut)
def get_current_user(current_user: models.User = Depends(oauth2.get_current_user)):
    return current_user
