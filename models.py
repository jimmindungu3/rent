# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

# Define the declarative base
Base = declarative_base()

# Define the Property model
class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False, unique=True)
    rent_amount = Column(Integer, nullable=False)
    tenants = relationship('Tenant', back_populates='property')

# Define the Tenant model
class Tenant(Base):
    __tablename__ = 'tenants'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    id_number = Column(String, nullable=False, unique=True)
    rent_payable = Column(Integer, nullable=False)
    property_id = Column(Integer, ForeignKey('properties.id'))
    property = relationship('Property', back_populates='tenants')
    rent_payments = relationship('RentPayment', back_populates='tenant')

# Define the RentPayment model
class RentPayment(Base):
    __tablename__ = 'rent_payments'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.now())
    details = Column(String)  # Adding a column for payment details
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    tenant = relationship('Tenant', back_populates='rent_payments')

# Define the database engine
engine = create_engine('sqlite:///rent_management.db')

# Create the tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Commit the changes
session.commit()

# You can run this script to create the database and its tables
print("Database tables created successfully.")
