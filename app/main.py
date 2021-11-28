from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='kerepakupai82',
            cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as err:
        print("Database connection failed")
        print(err)
        time.sleep(5)


app = FastAPI()

posts = [
    { "id": 1, "title": "my first posts", "content": "my first content" },
    { "id": 2, "title": "my second posts", "content": "my second content" }
]

def find_post(id):
    for p in posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return { "message": "Hello World!" }


@app.get("/posts")
async def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return { "data": posts }


# @app.get("/posts/latest")
# async def get_latest_post():
#    post = posts[len(posts)-1]
#    return { "data": post }


@app.get("/posts/{id}")
async def get_post(id: int):
    # post = find_post(id)
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return { "message": "Post does not found" }
    
    return { "data": post }


# @app.post("/posts")
# async def create_post(body: dict = Body(...)):
#    print(body)
#    return { "data": f"title {body['title']} content {body['content']}" }


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(1, 1000000)
    # print(post.dict())
    # posts.append(post_dict)
    cursor.execute(""" 
        INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
        (post.title, post.content, post.published))
    post = cursor.fetchone()
    conn.commit()

    return { "data": post }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    # index = find_index_post(id)
    cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING * """, (str(id)))
    post = cursor.fetchone()
    conn.commit()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found" )

    # posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    # index = find_index_post(id)
    cursor.execute(""" 
        UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", 
        (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    conn.commit()
    
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found" )

    # post_dict = post.dict()
    # post_dict['id'] = id
    # posts[index] = post_dict
    return { "data": post }