from fastapi import FastAPI, Request, Body, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import base_module

app = FastAPI() # <- Создаем экземпляр класса FastAPI
templates = Jinja2Templates(directory="templates")

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
    db, Person = base_module.create_open_base()
    users = db.query(Person).all()
    context = {}
    for user in users:
        new_el = {user.email: user.password}
        context.update(new_el)
    return templates.TemplateResponse("users.html", {"request": request, "context": context})

@app.post("/rec/")
async def add_us(data = Body()):
    db, Person = base_module.create_open_base()
    new_email = data["mail"]
    new_password = data["pass"]
    user = Person(email = new_email, password = new_password)
    db.add(user)
    db.commit()
    return RedirectResponse(url="/login/", status_code=status.HTTP_302_FOUND)
    
@app.post("/check/")
async def check_us(data = Body()):
    db, Person = base_module.create_open_base()
    new_email = data["mail"]
    new_password = data["pass"]
    users = db.query(Person).all()
    for user in users:
        if (user.email == new_email) and (user.password == new_password):
            return RedirectResponse(url="/enter/", status_code=status.HTTP_302_FOUND)
    else:
        return 'Такого пользователя нет. Зарегистрируйтесь.'
    
    


# uvicorn main:app --reload