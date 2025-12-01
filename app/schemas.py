from pydantic import BaseModel
from typing import Any, Optional, List
from datetime import date as DateType


# -------- Universal Response Format --------
class StandardResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[Any]] = None


# -------- Expense Schemas --------
class ExpenseBase(BaseModel):
    date: DateType
    category: str
    description: str
    amount: float


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    date: Optional[DateType] = None
    category: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None


class Expense(ExpenseBase):
    id: int

    model_config = {"from_attributes": True}  # IMPORTANT for SQLAlchemy ORM objects
