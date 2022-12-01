from fastapi import FastAPI,Response,status,HTTPException
#from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating:Optional[int] = None

while True:

    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi',
                                user='postgres',
                                password='Boulogne_1981',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("connection ok")
        break
    except Exception as err:
        print("Error : ",type(err))
        time.sleep(3)

my_posts = [{"title": "title post 1", "content": "content 1", "id": 1},
            {"title": "title post 2", "content": "content 2", "id": 2}]


def find_post(id):
    for p in my_posts:
        if id == p["id"]:
            return p


def find_index_post(id):
    for i,p in enumerate(my_posts):
        if id == p["id"]:
            return i


@app.get("/")
async def root():
    return {"message": "Hello Amaya"}


@app.get("/posts")
async def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()

    return {"data": posts}


@app.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", str(id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post with id : {%s} was not found" %id)

    return {"post_detail": post}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s,content = %s,published =%s 
    WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post with id : {%s} does not exist" %id)

    return {"data": updated_post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):

    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, str(id))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post with id : {%s} does not exist" %id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)