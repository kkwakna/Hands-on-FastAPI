from sqlalchemy import select
from sqlalchemy.orm import Session

from .orm import ToDo

def get_todos(session: Session):
    return list(session.scalars(select(ToDo)))

