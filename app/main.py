from typing import Optional
from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #note
    rating: Optional[int] = None #note

@app.get("/")
def root():
    return {"message": "Hello World darpan"}

@app.post("/posts", status_code=status.HTTP_201_CREATED) #note
def get_posts(new_post: Post): #payload: dict = Body(...)
    print(new_post)
    return {"message": new_post.title}

# get one post
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print("this is the id ", id)
    post = {"new post"}
    # if not post: #note: old way of doing things
    #     response.status_code = status.HTTP_404_NOT_FOUND
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"the id {id} not found")
    
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def get_post(id: int, response: Response):
    print("this is the id ", id)
    post = {"new post"}
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"the id {id} not found")
    
    return {"message": f"received the id as {id}"}

@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def get_post(id: int, post: Post, response: Response):
    print("this is the id ", id)
    post = {"new post"}
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"the id {id} not found")
    
    return {"message": f"received the id as {id}"}