from typing import List

from fastapi import Body, FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database.connection import get_db
from .database.orm import ToDo
from .database.repository import get_todos

app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"ping":"pong"}

# 조회를 위한 데이터 생성
todo_data = {
    1:{
        "id": 1,
        "contents": "실전! FastAPI 섹션 0 수강",
        "is_done": True,
    },
    2:{
        "id": 2,
        "contents": "실전! FastAPI 섹션 1 수강",
        "is_done": False,
    },
    3:{
        "id": 3,
        "contents": "실전! FastAPI 섹션 2 수강",
        "is_done": False,
    },
}

# 전체 데이터 조회, 쿼리 파라미터 추가
@app.get("/todos", status_code=200)
# 쿼리 파라미터: str 또는 None
def get_todos_handler(
    order: str | None = None,
    session: Session = Depends(get_db)
):
    todos: List[ToDo] = get_todos(session=session)

    # 쿼리 파라미터 값이 "DESC"인 경우 결과 역정렬 후 리턴
    if order and order == "DESC":
        return todos[::-1]
    # 아닌 경우, 바로 리턴
    return todos

#todos 아래에 {todo_id} path와 매핑
@app.get("/todos/{todo_id}", status_code=200)
# 입력 받은 {todo_id} 값으로 데이터 조회
def get_todo_handler(todo_id: int):
    todo = todo_data.get(todo_id)
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="Todo Not Found")

# request body 검증을 위한 pydantic model 설계
class CreateToDoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool

# 데이터 생성
@app.post("/todos", status_code=201)
# request pydantic 검증 후 
def create_todo_handler(request: CreateToDoRequest):
    # 새로운 데이터로 추가
    todo_data[request.id] = request.dict()
    # 추가한 데이터 리턴
    return todo_data[request.id]

# {todo_id}에 해당하는 데이터 수정
@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
    todo_id: int,
    # request body 하나의 컬럼 값을 사용할 수 있음
    is_done: bool = Body(..., embed=True)
):
    todo = todo_data.get(todo_id)
    # todo가 있다면
    if todo:
        # request 값으로 수정
        todo["is_done"] = is_done
        return todo
    # todo가 없다면
    raise HTTPException(status_code=404, detail="ToDo Not Found")

# 데이터 삭제
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int):
    # {todo_id}에 해당하는 데이터 삭제, 키 에러 방지(None: default value)
    todo = todo_data.pop(todo_id, None)
    if todo:
        return
    else:
        raise HTTPException(status_code=404, detail="ToDo Not Found")
