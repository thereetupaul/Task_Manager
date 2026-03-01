from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# database connection string
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# create automatically a connection pool to the database behind the scenes
engine = create_engine(SQLALCHEMY_DATABASE_URL)     #knows where the database is located & uses the default driver available in our environment (psycopg2 for postgresql)

# create new session & will request a connection from the pool
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# create a base class for our models
Base = declarative_base()

# dependency to get a database session
def get_db():               
    db = SessionLocal()
    try:
        yield db       #(yield)pause and let the request use the db session
    finally:
        db.close()     #after the request is finished, close the db session & return the connection to the pool



#connection test code (without SQLAlchemy)
'''
while True:
    try:
        conn = psycopg2.connect(host= 'localhost',port=5433, database='fastapi', user = 'postgres', password='password123', cursor_factory=RealDictCursor )
        cursor = conn.cursor()
        print("Database connection was successful!")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)
'''