from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import base_module

templates = Jinja2Templates(directory="templates")
db, Person, Task = base_module.create_open_base()

def decor_main(app):
    @app.get("/")
    async def index(request: Request):
        return templates.TemplateResponse(request=request, name='index.html')
    
def decor_login(app):
    @app.get("/login/")
    async def login(request:Request):
        return templates.TemplateResponse(request=request, name="login.html")
    
def decor_register(app):
    @app.get("/register/")
    async def login(request:Request):
        return templates.TemplateResponse(request=request, name="register.html")
    
def decor_users(app):
    @app.get("/users/", response_class = HTMLResponse)
    async def get_users_page(request:Request):
        users:list = db.query(Person).all()
        context:dict = {}
        i:int = 1
        for user in users:
            new_el = {str(i): user.name}
            context.update(new_el)
            i += 1
        return templates.TemplateResponse("users.html", {"request": request, "context": context})
    
def decor_tasks(app):
    @app.get("/tasks/{name}")
    async def get_tasks_page(request:Request, name:str):
        context = db.query(Person).filter(Person.name == name).one()
        return templates.TemplateResponse("tasks.html", {"request": request, "context": context})