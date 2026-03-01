from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional, Literal



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


#Response model for Post
class Post(PostBase):
    id: int                 # *schema field names must match ORM attributes*  
    owner_id: int           # means which field u r trying to return must be present in the model
    created_at: datetime
    owner : 'UserOut'  #nested response model

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr 
    password: str
    
#Response model for user for Orm mode
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True    


class UserLogin(BaseModel):
    email: EmailStr 
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir : Literal[0, 1]    #dir can only be 0 or 1   #Exact choices -> Literal (![1.The range matters,2.Values may expand later,3.Need numeric ordering])