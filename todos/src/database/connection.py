from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# root 유저의 todos 비밀번호, 로컬호스트의 3306 포트 이용, todos 데이터베이스 사용 
DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3306/todos"

# echo=True 옵션을 주면, SQLAlchemy가 실행하는 SQL문을 콘솔에 출력 (개발환경에서 디버깅용)
engine = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionFactory()

def get_db():
    session = SessionFactory()
    try: 
        yield session
    finally:
        session.close()
