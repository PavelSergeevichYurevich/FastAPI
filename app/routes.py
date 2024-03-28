from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import status
from sqlalchemy.orm import Session
from models import User, Task
from base_module import engine
from sqlalchemy import select
from schemas import UserCreateSchema, TaskCreateSchema, TaskUpdateSchema, TaskDeleteSchema, UserCheckSchema

tasks_router = APIRouter()
templates = Jinja2Templates(directory="templates")
 
@tasks_router.get('/')
async def index(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')

@tasks_router.get("/login/")
async def login(request:Request):
    return templates.TemplateResponse(request=request, name="login.html")

@tasks_router.get("/register/")
async def login(request:Request):
    return templates.TemplateResponse(request=request, name="register.html")

@tasks_router.get("/users/", response_class = HTMLResponse)
async def get_users_page(request:Request):
    with Session(engine) as session:
        stmnt = select(User)
        users:list = session.scalars(stmnt).all()
        context:dict = {}
        i:int = 1
        for user in users:
            new_el = {str(i): user.name}
            context.update(new_el)
            i += 1
        return templates.TemplateResponse("users.html", {"request": request, "context": context})
 
@tasks_router.get("/tasks/{name}")
async def get_tasks_page(request:Request, name:str):
     with Session(engine) as session:
        stmnt = select(User).where(User.name == name)
        context = session.scalars(stmnt).one()
        return templates.TemplateResponse("tasks.html", {"request": request, "context": context})
 
@tasks_router.post("/rec/")
async def add_us(request:Request, user: UserCreateSchema):
    with Session(engine) as session:
        print(user.email)
        print(type(user.email))
        new_user = User(email = user.email, password = user.password, name = user.name)
        session.add(new_user)
        session.commit()
    return RedirectResponse(url="/login/", status_code=status.HTTP_302_FOUND)

@tasks_router.post("/recTask/")
async def add_task(request:Request, task: TaskCreateSchema):
    name = task.user_name
    with Session(engine) as session:
        new_task = Task(task = task.task, describe = task.describe, ex_date = task.ex_date, user_name = task.user_name)
        session.add(new_task)
        session.commit()
    return RedirectResponse(url=f"/tasks/{name}", status_code=status.HTTP_302_FOUND)

@tasks_router.post("/taskChange/")
async def change_task(request:Request, task_upd: TaskUpdateSchema):
    name = task_upd.name
    with Session(engine) as session:
        stmnt = select(Task).where(Task.id == task_upd.id)
        task = session.scalars(stmnt).one()
        match task_upd.field:
            case 'task': task.task = task_upd.new_value
            case 'describe': task.describe = task_upd.new_value
            case 'ex_date': task.ex_date = task_upd.new_value
        session.add(task)
        session.commit()
    return RedirectResponse(url=f"/tasks/{name}", status_code=status.HTTP_302_FOUND)

@tasks_router.post("/taskDel/")
async def del_task(request:Request, task_del: TaskDeleteSchema):
    name = task_del.name
    with Session(engine) as session:
        stmnt = select(Task).where(Task.id == task_del.id)
        task = session.scalars(stmnt).one()
        session.delete(task)
        session.commit()
    return RedirectResponse(url=f"/tasks/{name}", status_code=status.HTTP_302_FOUND)

@tasks_router.post("/check/")
async def check_us(request:Request, checking_user: UserCheckSchema):
    with Session(engine) as session:
        stmnt = select(User)
        users:list = session.scalars(stmnt).all()
        for user in users:
            if (user.email == checking_user.email) and (user.password == checking_user.password):
                name = user.name
                return RedirectResponse(url=f"/tasks/{name}",status_code=status.HTTP_302_FOUND)
        else:
            return 'Такого пользователя нет. Зарегистрируйтесь.'