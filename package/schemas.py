from pydantic import BaseModel, validator
from pathlib import Path
from fastapi import File
from datetime import date


class users (BaseModel):
    username: str
    email: str
    password: str


class Questions(BaseModel):
    user: int
    question: str
    reply: str


class showQuestions (Questions):
    class Config():
        orm_mode = True


class Replies(BaseModel):
    question:  int
    reply:   str


class showReplies (Replies):
    class Config():
        orm_mode = True
