from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# url = postgresql://<username>:<password>@<ip_adress/hostname>/<database_name>'

url = f'postgresql://{settings.database_username}:{settings.database_password}@' \
      f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#
#     try:
#         conn = psycopg2.connect(host='localhost',
#                                 database='fastapi',
#                                 user='postgres',
#                                 password='Boulogne_1981',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("connection ok")
#         break
#     except Exception as err:
#         print("Error : ", type(err))
#         time.sleep(3)