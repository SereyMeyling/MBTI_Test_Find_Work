from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


db = SQLAlchemy()


DB_HOST = "localhost"      
DB_NAME = "mbti"  
DB_USER = "root"           
DB_PASS = ""               
DB_PORT = 3306           

# MySQL connection URL
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine
engine = create_engine(
    DB_URL,
    echo=True 
)

# Session setup
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base model
Base = declarative_base()


# Dependency for FastAPI / Flask session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()