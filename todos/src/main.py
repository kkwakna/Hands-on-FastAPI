from typing import List

from fastapi import Body, FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .schema.request import CreateToDoRequest
from .schema.response import ToDoListSchema, ToDoSchema
from .database.connection import get_db
from .database.orm import ToDo
from .database.repository import create_todo, get_todo_by_todo_id, get_todos, update_todo

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
) -> ToDoListSchema:
    todos: List[ToDo] = get_todos(session=session)

    # 쿼리 파라미터 값이 "DESC"인 경우 결과 역정렬 후 리턴
    if order and order == "DESC":  
        return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
    )
    # 아닌 경우, 바로 리턴
    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )

#todos 아래에 {todo_id} path와 매핑
@app.get("/todos/{todo_id}", status_code=200)
# 입력 받은 {todo_id} 값으로 데이터 조회
def get_todo_handler(
    todo_id: int, 
    session: Session = Depends(get_db)
)-> ToDoSchema:
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo Not Found")

# 데이터 생성
@app.post("/todos", status_code=201)
# request pydantic 검증 후 
def create_todo_handler(
    request: CreateToDoRequest,
    session: Session = Depends(get_db)
)-> ToDoSchema:
    todo: ToDo = ToDo.create(request=request)
    todo: ToDo = create_todo(session=session, todo=todo)

    # 추가한 데이터 리턴
    return ToDoSchema.from_orm(todo)

# {todo_id}에 해당하는 데이터 수정
@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
    todo_id: int,
    # request body 하나의 컬럼 값을 사용할 수 있음
    is_done: bool = Body(..., embed=True),
    session: Session = Depends(get_db),
):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        todo.done() if is_done else todo.undone()
        todo: ToDo = update_todo(session=session, todo=todo)
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo Not Found")    # todo가 있다면

# 데이터 삭제
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int):
    # {todo_id}에 해당하는 데이터 삭제, 키 에러 방지(None: default value)
    todo = todo_data.pop(todo_id, None)
    if todo:
        return
    else:
        raise HTTPException(status_code=404, detail="ToDo Not Found")
