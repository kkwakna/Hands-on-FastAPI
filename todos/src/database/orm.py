# orm은 데이터베이스 테이블과 매핑되는 클래스를 정의하는 모듈
# 실습: orm을 사용하여 데이터베이스 테이블을 조회
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base
from ..schema.request import CreateToDoRequest


### declarative_base()를 통해 Base 클래스 생성
Base = declarative_base()

class ToDo(Base):
    __tablename__ = "todo"
    
    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)

    ### __repr__() 메서드 오버라이딩. ToDo 객체 출력 확인용
    def __repr__(self): 
        return f"ToDo(id={self.id}, contents={self.contents}, is_done={self.is_done})"

    # orm 객체로 변환
    @classmethod
    def create(cls, request: CreateToDoRequest)->"ToDo":
        return cls(
            contents=request.contents,
            is_done=request.is_done
        )
    def done(self) -> "ToDo":
        self.is_done = True
        return self

    def undone(self) -> "ToDo":
        self.is_done = False
        return self
    
