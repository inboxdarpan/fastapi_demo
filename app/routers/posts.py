from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Users']
)
# create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) #note
def get_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db)): #payload: dict = Body(...)
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.published))
    # created_post = cursor.fetchone()
    # conn.commit()

    # using ORM
    # created_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published)

    # **new_post would do models.Post.title = new_post.title
    created_post = models.Post(**new_post.model_dump())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post
 
# get one post
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)): #response: Response was there where we tried editing the status code in the response

    # if not post: #note: old way of doing things
    #     response.status_code = status.HTTP_404_NOT_FOUND

    # doing it with usual DB    
    # db.execute("""SELECT * FROM posts WHERE id= %s """, (str(id),)) #note: a comma after val if it is >= 10
    # post = db.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first() #note: used db.query()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"the id {id} not found")
    
    return post

# get all posts
@router.get("/", response_model=List[schemas.Post]) #note: datatype List for List
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # cursor.execute("""SELECT * FROM posts  """)
    # # if not post: #note: old way of doing things
    # #     response.status_code = status.HTTP_404_NOT_FOUND
    # posts = cursor.fetchall()
    if posts == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"the id {id} not found")
    
    return posts



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def get_post(id: int, db: Session=Depends(get_db)):
    # cursor.execute("""DELETE FROM POSTS WHERE id=%s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    #note: only gives the query, gotta use .first(), .all() etc to actually execute it.
    deleted_post = db.query(models.Post).filter(models.Post.id == id) 
    # if deleted_post == None:
    if deleted_post.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"the id {id} not found")
    
    deleted_post.delete(synchronize_session=False) #note: used synchronize_session
    db.commit() #note
    return {"message": f"received the id as {id}"}

@router.put("/{id}", response_model=schemas.Post)
def get_post(id: int, new_post: schemas.Post, db: Session=Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", \
    #                (post.title, post.content, post.published, str(id)))
    # edited_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    # if edited_post == None:
    if post_query.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"the id {id} not found")
    
    #note used model_dump for dictionary, not **new_post, as it was doing the comparing thing, in create post
    post_query.update(new_post.model_dump(), synchronize_session=False) #note: used synchronize_session
    db.commit()
    
    return {"data": post_query.first()}

