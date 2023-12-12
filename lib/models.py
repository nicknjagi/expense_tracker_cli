from sqlalchemy import Column,Text, Integer,String, Boolean,ForeignKey,  DateTime
from sqlalchemy.orm import declarative_base, relationship
from config import engine

Base = declarative_base()
Base.metadata.create_all(engine)

class User(Base):
    pass


class Category(Base):
    pass


class Expense(Base):
    pass
