from fastapi import Request, Request, UploadFile, FastAPI, Depends, status, Response, HTTPException, File, Form
import os
from typing import Optional, List
from pydantic import BaseModel
from package import schemas, models
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from datetime import date

from package.database import engine, SessionLocal

models.Base.metadata.create_all(engine)

#uvicorn --host 192.168.1.2 --port 8007 main:app --reload

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATING WELLS

@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.users, db: Session = Depends(get_db)):
    new_user = models.Users(email=request.email, password=request.password, username=request.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/", status_code=status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    user = db.query(models.Users).all()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no user created yet")
    return user






@app.post("/questions/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Questions, db: Session = Depends(get_db)):
    new = models.Questions(user=request.user, question=request.question, reply=request.reply)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@app.get("/questions/", status_code=status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    quest = db.query(models.Questions).all()
    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no qstn created yet")
    return quest




@app.delete("/questions/", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    qstn = db.query(models.Questions).filter(models.Questions.id == id)
    if not qstn.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inexistant")
    qstn.delete(synchronize_session=False)
    db.commit()
    return "Deleted"


@app.post("/replies/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Replies, db: Session = Depends(get_db)):
    new = models.Replies(question=request.question, reply=request.reply)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@app.get("/replies/question/{id}", status_code=status.HTTP_200_OK)
def show(id, db: Session = Depends(get_db)):
    reply = db.query(models.Replies).filter(models.Replies.question == id).all()
    if not reply:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no reply with this question {id}")
    return reply


@app.get("/replies/", status_code=status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    reply = db.query(models.Replies).all()
    if not reply:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no reply created yet")
    return reply

@app.delete("/replies/", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    rep = db.query(models.Replies).filter(models.Replies.id == id)
    if not rep.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Inexistant")
    rep.delete(synchronize_session=False)
    db.commit()
    return "Deleted"
