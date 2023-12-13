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
        
