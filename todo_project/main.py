from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel

app = FastAPI()

# In-memory storage for tasks with type annotation
tasks: list[dict[str, int | str]] = []

# Define the Task model
class Task(BaseModel):
    id: int
    description: str
    status: str

# Define the TaskCreate model for input validation
class TaskCreate(BaseModel):
    description: str
    status: str = "in progress"  # default value

@app.get("/")
def read_root():
    return {"message": "Welcome to the To-Do List API"}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    # Explicitly specify types for Mypy
    new_task: dict[str, int | str] = {
        "id": len(tasks) + 1,
        "description": task.description,
        "status": task.status,
    }
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}", response_model=Task)  # Fixed missing leading slash
def update_task(task_id: int, updated_task: TaskCreate):
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = updated_task.description
            task["status"] = updated_task.status
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
