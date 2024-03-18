from sqlalchemy import create_engine, Integer, String, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

def create_open_base():
    engine = create_engine("sqlite:///./users.db")
    Base = declarative_base()   
    class Person(Base):
        __tablename__ = "users"
        id = Column(Integer(), primary_key=True, index=True)
        email = Column(String)
        password = Column(String) 
        name = Column(String)
        tasks = relationship("Task", backref='user')
        
    class Task(Base):
        __tablename__ = "tasks"
        id = Column(Integer, primary_key=True, index=True)
        task = Column(String)
        describe = Column(String) 
        ex_date = Column(String) 
        name_resp = Column(String, ForeignKey('users.name'))
        
    Base.metadata.create_all(bind=engine)
    # Base.metadata.drop_all(engine)
    SessionLocal = sessionmaker(autoflush=False, bind=engine)
    db = SessionLocal()
    return db, Person, Task

# create_open_base()