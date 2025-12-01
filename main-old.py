from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


class Expense(BaseModel):
    id: int
    date: str
    category: str
    description: str
    amount: float


class UpdateExpense(BaseModel):
    date: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None


expenses: List[Expense] = []


@app.get("/")
def home():
    return {"message": "Hello Rahul, your FastAPI is running 🚀"}


@app.post("/expenses")
def add_expense(expense1: Expense):
    expenses.append(expense1)
    return {"message": "Expense added successfully"}


@app.get("/expenses")
def get_all_expenses():
    if not expenses:
        return {"message": "No expenses found", "data": []}
    return {"message": "Success", "data": expenses}


@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    for e in expenses:
        if e.id == expense_id:
            return {"message": "Success", "data": e}
    return {"message": "Expense not found", "data": None}


@app.patch("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: UpdateExpense):
    for e in expenses:
        if e.id == expense_id:
            if expense.amount is not None:
                e.amount = expense.amount
            if expense.category is not None:
                e.category = expense.category
            if expense.description is not None:
                e.description = expense.description
            return {"message": "Expense updated successfully.", "data": e}

    return {"message": "Expense not found", "data": None}


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    for e in expenses:
        if e.id == expense_id:
            expenses.remove(e)
            return {"message": "Expense deleted successfully", "data": e}
    return {"message": "Expense not found", "data": None}
