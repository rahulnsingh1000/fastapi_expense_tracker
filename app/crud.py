from sqlalchemy.orm import Session
from . import models, schemas


def get_all_expenses(db: Session):
    expenses = db.query(models.Expense).all()
    return [
        schemas.Expense.model_validate(e) for e in expenses
    ]  # CONVERT ORM ➝ PYDANTIC


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
