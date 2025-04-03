import secrets

import uvicorn
from fastapi import FastAPI, Depends, Body, APIRouter, HTTPException
from typing import Optional, Annotated
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials, HTTPBasicCredentials

app1 = FastAPI()

task = []
id_task = 0
chet_task = 0

security = HTTPBasic()


class Prime_tsk(BaseModel):
    id: int
    Task: str


def auth(uchetka: HTTPBasicCredentials = Depends(security)):
    token="key"
    if uchetka.username=="token" and uchetka.password=="token":
        return uchetka
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"jj"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"jj"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app1.post("/post")
def create_task(Task: Optional[str] = "Task", user: str = Depends(get_current_username)):
    if Task is not None:
        global id_task
        id_task += 1
        obj = Prime_tsk(id=f"{id_task}", Task=Task)
        task.append(obj)
    else:
        return "Введи таск"
    return "good"

@app1.post("/post/Body")
def setBody(per = Body(... , embed=True)):
    return {"resp": "OK"}

@app1.get("/read_all")
def read_all():
    if task:
        return task
    else:
        return "Список пуст"


@app1.get("/read/{item}")
def read_item(id: int):
    for item in task:
        if id == item.id:
            iscom = item
    if iscom:
        return iscom
    else:
        return "Записи с таким id нет"


@app1.put("/put")
def put(id: int, new: str):
    for item in task:
        if id == item.id:
            item.Task = new
            iscom = item
    return iscom


@app1.delete("/delete")
def delete_task(id: int):
    for item in task:
        if id == item.id:
            task.remove(item)

if __name__=="__main__":
	uvicorn.run(app="api:app1", port=8008, reload=True, host="127.0.0.1")