from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Body, status
from sqlalchemy.orm import Session
from models import User, Task
from base_module import engine
from sqlalchemy import select

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
async def add_us(data = Body()):
    with Session(engine) as session:
        new_email = data["mail"]
        new_password = data["pass"]
        new_name = data["name"]
        user = User(email = new_email, password = new_password, name = new_name)
        session.add(user)
        session.commit()
    return RedirectResponse(url="/login/", status_code=status.HTTP_302_FOUND)

@tasks_router.post("/recTask/")
async def add_task(data = Body()):
    new_task = data["task"]
    new_describe = data["describe"]
    new_ex_date = data["ex_date"]
    new_user_name = data["user_name"]
    name = new_user_name
    with Session(engine) as session:
        task = Task(task = new_task, describe = new_describe, ex_date = new_ex_date, user_name = new_user_name)
        session.add(task)
        session.commit()
    return RedirectResponse(url=f"/tasks/{name}", status_code=status.HTTP_302_FOUND)

@tasks_router.post("/taskChange/")
async def change_task(data = Body()):
    id = data["id"]
    field = data["field"]
    new_value = data["new_value"]
    name = data["name"]
    with Session(engine) as session:
        stmnt = select(Task).where(Task.id == id)
        task = session.scalars(stmnt).one()
        match field:
            case 'task': task.task = new_value
            case 'describe': task.describe = new_value
            case 'ex_date': task.ex_date = new_value
        session.add(task)
        session.commit()
    return RedirectResponse(url=f"/tasks/{name}", status_code=status.HTTP_302_FOUND)

@tasks_router.post("/taskDel/")
async def del_task(data = Body()):
    id = data["id"]
    name = data["name"]
    with Session(engine) as session:
        stmnt = select(Task).where(Task.id == id)
        task = session.scalars(stmnt).one()
        session.delete(task)
        session.commit()
    return RedirectResponse(url=f"/tasks/{name}", status_code=status.HTTP_302_FOUND)

@tasks_router.post("/check/")
async def check_us(data = Body()):
    new_email = data["mail"]
    new_password = data["pass"]
    with Session(engine) as session:
        stmnt = select(User)
        users:list = session.scalars(stmnt).all()
        for user in users:
            if (user.email == new_email) and (user.password == new_password):
                name = user.name
                return RedirectResponse(url=f"/tasks/{name}",status_code=status.HTTP_302_FOUND)
        else:
            return 'Такого пользователя нет. Зарегистрируйтесь.'