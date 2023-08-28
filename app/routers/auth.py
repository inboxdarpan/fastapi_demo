from fastapi import requests, APIRouter, status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, utils, database, oauth2
router = APIRouter(tags=['Authentication'])

@router.get("/login", response_model=schemas.Token)
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    #note: using user_creds.username from fastapi.security.oauth2 library, THIS REQUIRED FORM DATA
    user = db.query(models.User).filter(models.User.email == user_creds.username).first() 

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    
    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentails")
    
    access_token = oauth2.crate_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


