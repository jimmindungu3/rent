# models/tenant.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Tenant(Base):
    __tablename__ = 'tenants'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    id_number = Column(String, nullable=False, unique=True)
    rent_payable = Column(Integer, nullable=False)
    property_id = Column(Integer, ForeignKey('properties.id'))
    property = relationship('Property', back_populates='tenants')
    rent_payments = relationship('RentPayment', back_populates='tenant')
