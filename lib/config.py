from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

# create engine
engine = create_engine("sqlite:///database.sqlite")

# create session
Session = sessionmaker(bind=engine)
session = Session()