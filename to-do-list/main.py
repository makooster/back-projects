from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()

from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")

class Task(BaseModel):
    id: int
    title: str
    description: str = None  # Optional field
    completed: bool = False

tasks = {}

@app.post("/tasks/")
def create_task(task: Task):
    if task.id in tasks:
        return {"error": "Task ID already exists"}
    tasks[task.id] = task.dict()
    return tasks[task.id]

@app.get("/tasks/")
def get_all_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return tasks.get(task_id, {"error": "Task not found"})

@app.put("/tasks/{task_id}")
def update_task_status(task_id: int, completed: bool):
    if task_id not in tasks:
        return {"error": "Task not found"}
    tasks[task_id]["completed"] = completed
    return tasks[task_id]

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id in tasks:
        del tasks[task_id]
        return {"message": "Task deleted successfully"}
    return {"error": "Task not found"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the To-Do API"}