from fastapi import FastAPI
import psycopg
import time
from . import models
from .database import engine
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        connection = psycopg.connect(
            host='localhost', dbname='fastapi', user='postgres', password='dinoel2362281337')
        cursor = connection.cursor()
        print('Database connection was sucessfull!')
        break
    except Exception as error:
        print('Database connection failed!')
        print(f'Error: {error}')
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
