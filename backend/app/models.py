from sqlalchemy import Column, ForeignKey , Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.orm import relationship

# define a model class for the "tasks" table
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="pending")
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False)

    owner = relationship("User")  #relationship to User model -> nothing to do with db table
    

#define a model for user registration
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, default="user")
    username = Column(String, nullable=True, unique=True)
    
    
    


