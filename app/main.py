from fastapi import FastAPI, Request, Body, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import base_module

app = FastAPI() # <- Создаем экземпляр класса FastAPI
templates = Jinja2Templates(directory="templates")
db, Person, Task = base_module.create_open_base()

@app.get("/") # <- декоратор, который обрабатывает get - запросы где маршрут
async def index(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')

@app.get("/login/") # <- декоратор, который обрабатывает get - запросы где маршрут
async def login(request:Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/register/") # <- декоратор, который обрабатывает get - запросы где маршрут
async def login(request:Request):
    return templates.TemplateResponse(request=request, name="register.html")

@app.get("/enter/") # <- декоратор, который обрабатывает get - запросы где маршрут
async def enter(request:Request):
    return templates.TemplateResponse("enter.html", {"request": request})
 
@app.get("/users/", response_class = HTMLResponse) # <- декоратор, который обрабатывает get - запросы где маршрут
async def get_users_page(request:Request):
    users:list = db.query(Person).all()
    context:dict = {}
    i:int = 1
    for user in users:
        new_el = {str(i): user.name}
        context.update(new_el)
        i += 1
    return templates.TemplateResponse("users.html", {"request": request, "context": context})

@app.get("/tasks/{name}") # <- декоратор, который обрабатывает get - запросы где маршрут
async def get_tasks_page(request:Request, name):
    context = db.query(Person).filter(Person.name == name).one()
    return templates.TemplateResponse("tasks.html", {"request": request, "context": context})

@app.post("/rec/")
async def add_us(data = Body()):
    new_email = data["mail"]
    new_password = data["pass"]
    new_name = data["name"]
    user = Person(email = new_email, password = new_password, name = new_name)
    db.add(user)
    db.commit()
    return RedirectResponse(url="/login/", status_code=status.HTTP_302_FOUND)

@app.post("/recTask/")
async def add_task(data = Body()):
    new_task = data["task"]
    new_describe = data["describe"]
    new_ex_date = data["ex_date"]
    new_name_resp = data["name_resp"]
    name = new_name_resp
    task = Task(task = new_task, describe = new_describe, ex_date = new_ex_date, name_resp = new_name_resp)
    db.add(task)
    db.commit()
    return RedirectResponse(url=f"/tasks/{name}", status_code=status.HTTP_302_FOUND)

@app.post("/taskChange/")
async def add_task(data = Body()):
    id = data["id"]
    field = data["field"]
    new_value = data["new_value"]
    name = data["name"]
    task = db.query(Task).get(id)
    match field:
        case 'task': task.task = new_value
        case 'describe': task.describe = new_value
        case 'ex_date': task.ex_date = new_value
    db.add(task)
    db.commit()
    return RedirectResponse(url=f"/tasks/{name}", status_code=status.HTTP_302_FOUND)

@app.post("/taskDel/")
async def add_task(data = Body()):
    id = data["id"]
    name = data["name"]
    task = db.query(Task).get(id)
    db.delete(task)
    db.commit()
    return RedirectResponse(url=f"/tasks/{name}", status_code=status.HTTP_302_FOUND)
    
@app.post("/check/")
async def check_us(data = Body()):
    new_email = data["mail"]
    new_password = data["pass"]
    users = db.query(Person).all()
    for user in users:
        if (user.email == new_email) and (user.password == new_password):
            name = user.name
            return RedirectResponse(url=f"/tasks/{name}",status_code=status.HTTP_302_FOUND)
    else:
        return 'Такого пользователя нет. Зарегистрируйтесь.'
    
    

# cd /var/www/FastAPI
# uvicorn main:app --host 127.0.0.1 --port 8000 --reload
# uvicorn main:app --reload