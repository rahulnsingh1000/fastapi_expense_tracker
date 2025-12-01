from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional
from datetime import date
from sqlalchemy import func


def get_all_expenses(
    db: Session,
    page: int,
    limit: int,
    category: Optional[str] = None,
    amount: Optional[float] = None,
    description: Optional[str] = None,
    date: Optional[date] = None
):
    query = db.query(models.Expense)

    # Apply optional filters dynamically
    if category:
        query = query.filter(
        func.lower(models.Expense.category) == category.lower()
    )

    if amount is not None:
        query = query.filter(models.Expense.amount == amount)

    if description:
        query = query.filter(models.Expense.description.contains(description))

    if date:
        query = query.filter(models.Expense.date == date)

    # Pagination
    total_items = query.count()
    total_pages = total_items // limit + (1 if total_items % limit > 0 else 0)

    expenses = query.offset((page - 1) * limit).limit(limit).all()

    pagination = {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "total_items": total_items,
        "has_next": page < total_pages,
        "has_previous": page > 1
    }

    return {
        "data": [schemas.Expense.model_validate(e) for e in expenses],
        "pagination": pagination
    }


def get_expense(db: Session, expense_id: int):
    expense =  db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        return None
    return [
        schemas.Expense.model_validate(expense)
    ] 


def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return schemas.Expense.model_validate(db_expense)


def update_expense(db: Session, expense_id: int, expense: schemas.ExpenseUpdate):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()   # get the expense by id

    if not db_expense:
        return None
    update_data = expense.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_expense, key, value)
    db.commit()
    return schemas.Expense.model_validate(db_expense)


# -----------------------------------------
#            DELETE (204 NO CONTENT)
# -----------------------------------------
def delete_expense(db: Session, expense_id: int):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not db_expense:
        return None
    db.delete(db_expense)
    db.commit()
    return True
