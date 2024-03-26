from fastapi import Body, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import base_module

templates = Jinja2Templates(directory="templates")
db, Person, Task = base_module.create_open_base()

def decor_add_user(app):
    @app.post("/rec/")
    async def add_us(data = Body()):
        new_email = data["mail"]
        new_password = data["pass"]
        new_name = data["name"]
        user = Person(email = new_email, password = new_password, name = new_name)
        db.add(user)
        db.commit()
        return RedirectResponse(url="/login/", status_code=status.HTTP_302_FOUND)
    
def decor_add_task(app):
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
    
def decor_change_task(app):
    @app.post("/taskChange/")
    async def change_task(data = Body()):
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
    
def decor_delete_task(app):
    @app.post("/taskDel/")
    async def del_task(data = Body()):
        id = data["id"]
        name = data["name"]
        task = db.query(Task).get(id)
        db.delete(task)
        db.commit()
        return RedirectResponse(url=f"/tasks/{name}", status_code=status.HTTP_302_FOUND)
    
def decor_check_user(app):
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