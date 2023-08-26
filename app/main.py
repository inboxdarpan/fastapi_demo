from typing import Optional
from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', \
                                user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connected")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error", error)
        time.sleep(2)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #note
    rating: Optional[int] = None #note

@app.get("/")
def root():
    return {"message": "Hello World darpan"}

# create post
@app.post("/posts", status_code=status.HTTP_201_CREATED) #note
def get_posts(new_post: Post): #payload: dict = Body(...)
    post_dict = new_post.model_dump()
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

# get one post
@app.get("/posts/{id}")
def get_post(id: int): #response: Response was there where we tried editing the status code in the response
    # print("this is the id ", id)
    cursor.execute("""SELECT * FROM posts WHERE id= %s """, (str(id),)) #note: a comma after val if it is >= 10
    post = cursor.fetchone()
    # if not post: #note: old way of doing things
    #     response.status_code = status.HTTP_404_NOT_FOUND
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"the id {id} not found")
    
    return {"data": post}

# get all posts
@app.get("/posts")
def get_all_posts():
    cursor.execute("""SELECT * FROM posts  """)
    # if not post: #note: old way of doing things
    #     response.status_code = status.HTTP_404_NOT_FOUND
    posts = cursor.fetchall()
    print(posts)
    if posts == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"the id {id} not found")
    
    return {"post_detail": posts}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def get_post(id: int):
    cursor.execute("""DELETE FROM POSTS WHERE id=%s RETURNING * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"the id {id} not found")
    
    return {"message": f"received the id as {id}"}

@app.put("/posts/{id}")
def get_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", \
                   (post.title, post.content, post.published, str(id)))
    edited_post = cursor.fetchone()
    conn.commit()
    if edited_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"the id {id} not found")
    
    return {"data": edited_post}