from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,utils
from ..oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm  
#OAuth2PasswordRequestForm -> extracts login credentials from the request body in OAuth2 format 
# Not in JSON body format but as form data 
#That's why we need Depends() -> to run OAuth2 form parser

router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    #OAuth2PasswordRequestForm has username and password fields
    #{"username": "email", 
    # "password": "password"}

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.Verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    
    #create a token 
    #return token
    
    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}