#!/usr/bin/env python

from config import session
from models import User, Expense, Category

def create_user(first_name , last_name , phone_number ):
    first_name = first_name
    last_name = last_name
    phone_number = phone_number
    user = User(
        first_name = first_name,
        last_name = last_name,
        phone_number = phone_number
    )
    session.add(user)
    session.commit()
    return user

def search_user(id):
    user = session.query(User).filter(User.id == id).first()

    if user:
        return user
    else:
        print(f'No user with id {id} found.\n') 

def delete_user(id):
    user = session.query(User).filter(User.id == id)
    if user.first():
        print(f"Deleted User => {user.first().first_name}, ID => {user.first().id}\n")
        user.delete()
        session.commit()
        return user
    else:
        print(f'No user with id {id} found.\n') 
        
if __name__ == "__main__":
    print("\n>>>>>>>>>>>> USER OPERATIONS <<<<<<<<<<<\n")
    print(f"{'*' * 6} Creating new user {'*' * 6}")
    user = create_user('John', 'Snow', '+254-756864')
    print(f'Created User => {user.first_name}\n')
    
    print(f"{'*' * 6} fetching user by id {'*' * 6}")
    retreived_user = search_user(5)
    print(retreived_user)
    print('')
    
    print(f"{'*' * 6} deleting user by id {'*' * 6}")
    deleted_user = delete_user(36)