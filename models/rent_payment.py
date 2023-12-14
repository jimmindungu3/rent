# models/rent_payment.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class RentPayment(Base):
    __tablename__ = 'rent_payments'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.now())
    details = Column(String)  # Adding a column for payment details
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    tenant = relationship('Tenant', back_populates='rent_payments')

