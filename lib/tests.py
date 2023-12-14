#!/usr/bin/env python

from config import session
from models import User, Expense, Category
from sqlalchemy import func

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
        
def get_users():
    all_users = session.query(User).all()
    for user in all_users:
        print(f'{user}')
    print('') 
    
def get_categories():
    categories = session.query(Category).all()
    for category in categories:
        print(f'{category}')
    print('') 

def search_category(name):
    category = session.query(Category).filter(Category.name == name).first()
    if category:
        print(category)   
    else:
        print(f'No category named {name} found.') 
    print('')
    
def create_expense(amount, description, user_id, category):
    category_id = session.query(Category).filter(Category.name == category).first().id
    
    expense = Expense(
        amount=amount,
        description = description,
        user_id = user_id,
        category_id = category_id
    )
    session.add(expense)
    session.commit()
    print('Expense has been recorded')
    print(expense)
    print('')
    return expense

def list_user_expenses(id):
    user = session.query(User).filter(User.id == id).first()
    print(f'\nExpenses for {user.first_name} {user.last_name}\n')
    
    expenses = user.expenses
    for expense in expenses:
        print(expense)
    print('')
    
def user_expenses_categories(id):
    user = session.query(User).filter(User.id == id).first()
    print(f'\nExpense categories for {user.first_name} {user.last_name}')
    
    categories = user.categories
    for category in categories:
        print(category)
    print('')
    
def get_expenses():
    expenses = session.query(Expense).limit(20).all()
    
    for expense in expenses:
        print(expense)       
    print('')
    
def user_category_spending(user_id):
    category_amount = (
        session.query(Category.name, func.sum(Expense.amount))
        .join(Expense)
        .filter(Expense.user_id == user_id)
        .group_by(Category.name)
        .all()
        )
    user = session.query(User).filter(User.id == user_id).first()
    print(f'\nCategory wise spending for {user.first_name} {user.last_name}')
    print('')
    for category, amount in category_amount:
        bar = '#' * int(amount / 15)
        print(f"Category: {category:15}, Total Spending: {amount} {bar}")
    print('')


        
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
    
    print(f"{'*' * 6} getting all users {'*' * 6}")
    get_users()
    
    print(f"{'*' * 6} getting all categories {'*' * 6}")
    get_categories()
    
    print(f"{'*' * 6} searching category by name {'*' * 6}")
    search_category('food')
    
    print(f"{'*' * 6} Creating new expense {'*' * 6}")
    expense = create_expense(100, 'bought a toothbrush', 5, 'utilities')

    print(f"{'' * 6} getting first 20 expenses {'' * 6}")
    get_expenses()
    
    print(f"{'*' * 6} Listing all user expenses {'*' * 6}")
    list_user_expenses(7)
    
    print(f"{'*' * 6} Getting all expenses for a user {'*' * 6}")
    user_expenses_categories(8)

    print(f"{'*' * 6} Getting category wise spending for user {'*' * 6}")
    user_category_spending(8)
    