from pydantic import BaseModel, EmailStr, conint
from typing import Optional, Literal



class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[Literal['pending', 'in progress', 'completed']] = 'pending'  #default status is pending, other statuses are optional


class TaskCreate(TaskBase):
    pass


#Response model for Task
class TaskOut(TaskBase):
    id: int                 # *schema field names must match ORM attributes*  
    owner_id: int           # means which field u r trying to return must be present in the model
    owner : 'UserOut'  #nested response model

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr 
    password: str
    username: Optional[str] = None
    role: Optional[Literal['user', 'admin']] = 'user'  #default role is user, admin is optional
    
#Response model for user for Orm mode
class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: Optional[str] = None
    role: Literal['user', 'admin']  #role is required in the response

    class Config:
        from_attributes = True    


class UserLogin(BaseModel):
    email: EmailStr 
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None






