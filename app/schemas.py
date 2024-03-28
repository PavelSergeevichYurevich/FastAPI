from pydantic import BaseModel

class UserCreateSchema(BaseModel):
    email: str
    password: str
    name: str
    
class UserCheckSchema(BaseModel):
    email: str
    password: str
    
class TaskCreateSchema(BaseModel):
    task: str
    describe: str
    ex_date: str
    user_name: str
    
class TaskUpdateSchema(BaseModel):
    id: int
    field: str
    new_value: str
    name: str
    
class TaskDeleteSchema(BaseModel):
    id: int
    name: str