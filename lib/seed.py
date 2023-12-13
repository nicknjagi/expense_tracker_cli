#!/usr/bin/env python

import random
from faker import Faker
from config import session
from models import User, Expense, Category

if __name__ == "__main__":
    session.query(User).delete()
    session.query(Expense).delete()
    session.query(Category).delete()
    
    fake = Faker()
    
    users = []
    for i in range(30):
        user = User(
            first_name = fake.unique.first_name(),
            last_name = fake.unique.last_name(),
            phone_number = fake.unique.phone_number()
        )
        
        session.add(user)
        session.commit()
        users.append(user)
    
    category_list = ['furniture','healthcare','utilities', 'restaurants', 'food', 'transportation', 'mortgage', 'clothing']
    categories = []
    for category in category_list:
        new_category = Category(
            name = category
        )
        session.add(new_category)
        session.commit()
        
        categories.append(new_category)
        
    expenses = []
    for user in users:
        for i in range(random.randint(1,5)):
            category = random.choice(categories)
            if user not in category.users:
                category.users.append(user)
                session.add(category)
                session.commit()
        
            expense = Expense(
                amount = random.randint(100,500),
                date = fake.date_time_this_year(),
                description = fake.sentence(nb_words=6),
                category_id = category.id,
                user_id = user.id
            )
        
            expenses.append(expense)
        
    session.add_all(expenses)
    session.commit()
    session.close()