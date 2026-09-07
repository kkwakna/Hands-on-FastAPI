from sqlalchemy import select
from sqlalchemy.orm import Session

from .orm import ToDo

def get_todos(session: Session):
    return list(session.scalars(select(ToDo)))

def get_todo_by_todo_id(session: Session, todo_id: int) -> ToDo | None:
    return session.scalars(select(ToDo).where(ToDo.id == todo_id)).first()

def create_todo(session: Session, todo: ToDo)-> ToDo:
    # 세션에 새 데이터 추가
    session.add(instance=todo)
    # 데이터베이스에 저장
    session.commit()
    # 데이터베이스 읽어옴. todo id 값이 자동 생성됨.
    session.refresh(instance=todo)
    return todo

def update_todo(session: Session, todo: ToDo)-> ToDo:
    session.add(instance=todo)
    # 데이터베이스에 저장
    session.commit()
    # 데이터베이스 읽어옴. todo id 값이 자동 생성됨.
    session.refresh(instance=todo)
    return todo

