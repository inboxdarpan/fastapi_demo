from typing import Optional, List
from fastapi import FastAPI, status, HTTPException, Response, Depends
# from fastapi.params import Body
import psycopg2

from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import models, schemas, utils
from .database import SessionLocal, engine, get_db
from .routers import users, posts

#learn pagination
# rate limiting
# authentication

models.Base.metadata.create_all(bind=engine) #note
app = FastAPI()

# Older way of making a database connection
# while True:
#     try:
#         # pass
#         conn = psycopg2.connect(host='localhost', database='fastapi', \
#                                 user='postgres', password='postgres', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database connected")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error", error)
#         time.sleep(2)

app.include_router(users.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Hello World darpan"}

