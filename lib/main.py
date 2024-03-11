#!/usr/bin/env python

from config import session
from models import User, Expense, Category
import click
from sqlalchemy import func
from tabulate import tabulate


@click.group()
def cli():
    pass

@cli.command()
def create_user():
    first_name = click.prompt(click.style("First name", fg="blue", bold=True))
    last_name = click.prompt(click.style("Last name", fg="blue", bold=True))
    phone_number = click.prompt(click.style("Phone number", fg="blue", bold=True))
    user = User(
        first_name = first_name,
        last_name = last_name,
        phone_number = phone_number
    )  
    
    session.add(user)
    session.commit()
    click.secho('User has been created',fg="green", bold=True)
    click.secho(user, fg='magenta')
    print("")  

@cli.command()
def search_user():
    id = click.prompt(click.style("Enter the user id", fg="blue", bold=True))
    user = session.query(User).filter(User.id == id).first()

    if user:
        click.secho(user, fg='magenta')
    else:
        click.secho(f'No user with id {id} found.', fg='white') 
    print("")  
        
@cli.command()
def delete_user():
    id = click.prompt(click.style("Enter the user id", fg="blue", bold=True))
    user = session.query(User).filter(User.id == id)
    if user.first() != None:
        user.delete()
        session.commit()
        click.secho('The user has been deleted.', fg="red")   
    else:
        click.secho(f'No user with id {id} found.', fg='white') 
    print("")  
    
@cli.command()
def get_users():
    all_users = session.query(User).all()
    click.secho('Showing all users\n', fg='yellow', underline=True)
     # Ensure all_users is a list of User objects
    if all_users:
        # Extract data from User objects and format it into a list of tuples
        user_data = [(user.id, user.fullName(), user.phone_number) for user in all_users]
        # Print tabulated data
        print(tabulate(user_data, headers=['ID', 'Name', 'Phone Number'], tablefmt='pretty'))
        print("")  
    else:
        click.echo('No users found.')
        print("")  
        
        
@cli.command()
def get_categories():
    categories = session.query(Category).all()
    click.secho('showing all categories', fg='yellow', underline=True, overline=True)
    category_data = [(category.id, category.name) for category in categories]
    print(tabulate(category_data, headers=['ID', 'Name'], tablefmt='pretty'))
    print("")  
    
@cli.command()
def create_expense():
    amount = click.prompt(click.style("Enter the amount", fg="blue", bold=True))
    description = click.prompt(click.style("Enter the description", fg="blue", bold=True))
    user_id = click.prompt(click.style("Enter the user id", fg="blue", bold=True))
    category= click.prompt(click.style("Enter the category", fg="blue", bold=True))
    category_id = session.query(Category).filter(Category.name == category).first().id
    
    expense = Expense(
        amount=amount,
        description = description,
        user_id = user_id,
        category_id = category_id
    )
    session.add(expense)
    session.commit()
    click.secho('Expense has been recorded',fg="green", bold=True)
    click.secho(expense, fg='magenta')
    print("")

@cli.command()
def list_user_expenses():
    id = click.prompt(click.style("Enter the user id", fg="blue", bold=True))
    user = session.query(User).filter(User.id == id).first()
    click.secho(f'\nExpenses for {user.first_name} {user.last_name}', fg='yellow')
    
    expenses = user.expenses
    expense_data = [(expense.id, expense.amount, expense.date.date(), expense.description, expense.category_id) for expense in expenses]
    print(tabulate(expense_data, headers=['ID', 'Amount', 'Date', 'Description'], tablefmt='pretty'))
    print('')

@cli.command()
def user_expenses_categories():
    id = click.prompt(click.style("Enter the user id", fg="blue", bold=True))
    user = session.query(User).filter(User.id == id).first()
    click.secho(f'\nExpense categories for {user.first_name} {user.last_name}', fg='yellow')
    
    categories = user.categories
    category_data = []

    for category in categories:
        # Check if there are expenses associated with the category
        category_expenses = session.query(Expense).filter_by(user_id=user.id, category_id=category.id).first()
        if category_expenses:
            category_data.append((category.name,))
    
    if category_data:
        print(tabulate(category_data, headers=['Categories'], tablefmt='pretty'))
    else:
        click.echo('No expenses found for any category.')
        
    print('')      
        
@cli.command
def get_expenses():
    expenses = session.query(Expense).all()
    
    click.secho('Showing all expenses', fg='yellow', underline=True)
    expense_data = [(expense.id, expense.amount, expense.date.date(), expense.description) for expense in expenses]
    print(tabulate(expense_data, headers=['ID', 'Amount', 'Date', 'Description'], tablefmt='pretty'))
        
    print('')

@cli.command()
def user_category_spending():
    user_id = click.prompt(click.style("Enter the user id", fg="blue", bold=True))
    category_amount = (
        session.query(Category.name, func.sum(Expense.amount))
        .join(Expense)
        .filter(Expense.user_id == user_id)
        .group_by(Category.name)
        .all()
        )
    user = session.query(User).filter(User.id == user_id).first()

    click.secho(f'\nCategory wise spending for {user.first_name} {user.last_name}', fg='yellow')
    print('')
    for category, amount in category_amount:
        bar = '#' * int(amount / 15)
        click.secho(f"Category: {category:15} Total Spending: {amount} {bar}", fg='cyan')
    print('')    

if __name__ == "__main__":
    click.secho(f'\n{"-" * 30} EXPENSE TRACKER {"-" * 30}\n', bold=True, fg='bright_cyan')
    
    cli()