from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    category = Column(String(50))
    description = Column(String(255))
    amount = Column(Float)
