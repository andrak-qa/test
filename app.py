from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

app = FastAPI()

# Фейковые БД
users_db = {}
tasks_db = {}


class User(BaseModel):
    id: int
    name: str
    email: str


class Task(BaseModel):
    id: int
    user_id: int
    status: str = 'pending'


@app.post('/users')
async def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail='User already exists')
    users_db[user.id] = user
    return user


@app.get('/users/{user_id}')
async def get_user(user_id: int):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@app.post('/tasks')
async def create_task(task: Task):
    if task.user_id not in users_db:
        raise HTTPException(status_code=400, detail='User does not exist')
    tasks_db[task.id] = task
    asyncio.create_task(process_task(task.id))
    return task


@app.get('/tasks/{task_id}')
async def get_task(task_id: int):
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    return task


async def process_task(task_id: int):
    await asyncio.sleep(5)  # Эмуляция выполнения задачи
    tasks_db[task_id].status = 'done'
