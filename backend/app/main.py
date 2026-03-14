from fastapi import FastAPI
import fastapi
from .database import engine
from . import models
from .routers import task,user,auth
from .config import settings
from fastapi.middleware.cors import CORSMiddleware   

print(settings.secret_key)  # Accessing the database_username from settings

#models.Base.metadata.create_all(bind=engine)   #create the database tables

app=FastAPI()

origins = ["*"]  # Allow all origins, you can specify specific origins if needed  

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#as we're using alembic for database migrations, we don't need to create tables using this line of code. We can use alembic to create and manage our database schema instead.
#models.Base.metadata.create_all(bind=engine)   #create the database tables   



app.include_router(task.router)
app.include_router(user.router)
app.include_router(auth.router)



@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!!!!!"}  


