from fastapi import FastAPI
import func_get, func_post
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory=Path(__file__).parent.absolute() / "static"), name="static")

func_get.decor_main(app)
func_get.decor_login(app)
func_get.decor_register(app)
func_get.decor_users(app)
func_get.decor_tasks(app)

func_post.decor_add_user(app)
func_post.decor_add_task(app)
func_post.decor_change_task(app)
func_post.decor_delete_task(app)
func_post.decor_check_user(app)


""" HOST = '127.0.0.1'
if __name__ == '__main__':
    # Model.metadata.create_all(engine)
    TaskModel.metadata.create_all(engine)
    print('Starting server')
    uvicorn.run('main:app', port=8000, host=HOST, reload=True)
    print('Server stopped') """

# cd /var/www/FastAPI
# uvicorn main:app --host 127.0.0.1 --port 8000 --reload
# uvicorn main:app --reload """