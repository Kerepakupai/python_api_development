from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)


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

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)