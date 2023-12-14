from sqlalchemy import Column,Text, Integer,String, func,ForeignKey,  DateTime, MetaData,Table
from sqlalchemy.orm import declarative_base, relationship ,backref
from config import engine


convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)
Base.metadata.create_all(engine)


user_category = Table(
    'user_categories',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('category_id', ForeignKey('categories.id'), primary_key=True),
    extend_existing=True
)
class User(Base):
    __tablename__="users"
    id=Column(Integer(), primary_key=True)
    first_name= Column(String())
    last_name=Column(String()) 
    phone_number=Column(Integer())
        
    
    expenses = relationship("Expense", backref=backref("user"))
    categories = relationship("Category",secondary=user_category, back_populates="users")
    
    def __repr__(self):
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, phone_number={self.phone_number})"


class Category(Base):
    __tablename__="categories"
    id=Column(Integer(), primary_key=True)
    name= Column(String())
    
    expenses = relationship("Expense",backref=backref("category"))
    users = relationship("User",secondary=user_category, back_populates="categories")
    
    def __repr__(self):
        return f"Category(id={self.id}, name={self.name})"


class Expense(Base):
    __tablename__="expenses"
    id=Column(Integer(), primary_key=True)
    amount= Column(Integer())
    description=Column(Text) 
    date=Column(DateTime(),default=func.now())
    
    
    user_id=Column(Integer(),ForeignKey("users.id"))
    category_id=Column(Integer(),ForeignKey("categories.id"))
    
    def __repr__(self):
        return f"Expense(id={self.id},amount={self.amount},date={self.date},description={self.description}"
    
    
    

