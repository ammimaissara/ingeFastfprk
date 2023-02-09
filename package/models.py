from sqlalchemy import Date, Date, Column, Integer, String, ForeignKey
from package.database import Base
from sqlalchemy.orm import relationship
from datetime import date

# for the sql


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    usernmae = Column(String)
    email = Column(String)
    password = Column(String)
    userQuest = relationship("Questions", back_populates="fk_user")


class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey('users.id'))
    question = Column(String)
    reply = Column(String)
    fk_user = relationship("Users", back_populates="userQuest")
    qstRep = relationship("Replies", back_populates="fk_qstn")

    
class Replies(Base):
    __tablename__ = 'replies'
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Integer, ForeignKey('questions.id'))
    reply = Column(String)
    fk_qstn = relationship("Questions", back_populates="qstRep")
