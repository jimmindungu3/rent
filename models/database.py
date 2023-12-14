# models/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base 

Base = declarative_base()
engine = create_engine('sqlite:///models/rent_management.db')
Session = sessionmaker(bind=engine)
session = Session()

print("Before creating tables")
# Create the database tables
Base.metadata.create_all(engine)
print("After creating tables")

