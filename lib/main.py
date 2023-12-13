#!/usr/bin/env python

from config import session
from models import User, Expense, Category
import click


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
    return user

@cli.command()
def search_user():
    id = click.prompt(click.style("Enter the user id", fg="blue", bold=True))
    user = session.query(User).filter(User.id == id).first()

    if user:
        click.secho(user, fg='magenta')
        return user
    else:
        click.secho(f'No user with id {id} found.', fg='white')  
        
        
if __name__ == "__main__":
    click.secho(f'\n{"-" * 30} EXPENSE TRACKER {"-" * 30}\n',overline=False, underline=False,bold=True, fg='bright_cyan')
    
    cli()