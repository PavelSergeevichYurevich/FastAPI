from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column, Integer, String
from sqlalchemy.orm import sessionmaker

def create_open_base():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base = declarative_base()   
    class Person(Base):
        __tablename__ = "Users"
        id = Column(Integer, primary_key=True, index=True)
        email = Column(String)
        password = Column(String) 
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autoflush=False, bind=engine)
    db = SessionLocal()
    return db, Person