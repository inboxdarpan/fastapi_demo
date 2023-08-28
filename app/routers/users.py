from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, database, oauth2

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", response_model=schemas.UserCreate, status_code=status.HTTP_201_CREATED)
def create_user(new_user:schemas.UserCreate, db: Session= Depends(database.get_db)):

    hashed_password = utils.hash(new_user.password)
    new_user.password = hashed_password
    created_user = models.User(**new_user.model_dump())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)

    return created_user

@router.get("/{id}", response_model=schemas.UserCreate)
def get_user(id:int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with ID {id} not found')
    
    return user
