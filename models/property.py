# models/property.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False, unique=True)
    rent_amount = Column(Integer, nullable=False)
    tenants = relationship('Tenant', back_populates='property')
