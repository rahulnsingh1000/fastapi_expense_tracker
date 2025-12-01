from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import crud, schemas, database
from ..schemas import StandardResponse
from fastapi.responses import JSONResponse
from typing import Optional

router = APIRouter(prefix="/expenses", tags=["Expenses"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------------------
#             GET ALL (200 OK)
# -----------------------------------------
@router.get("/", response_model=StandardResponse, status_code=status.HTTP_200_OK)
def get_expenses(db: Session = Depends(get_db), page: int = 1, limit: int = 10, category: Optional[str] = None, amount: Optional[float] = None, description: Optional[str] = None, date: Optional[date] = None):
    expenses = crud.get_all_expenses(db, page, limit, category, amount, description, date)
    pagination = expenses["pagination"]
    return StandardResponse(
        success=True,
        message="Expenses fetched successfully",
        data=expenses["data"],
        pagination=pagination,
    )


# -----------------------------------------
#          CREATE (201 CREATED)
# -----------------------------------------
@router.post("/", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = crud.create_expense(db, expense)
    return StandardResponse(
        success=True,
        message="Expense created successfully",
        data=new_expense,
    )


# -----------------------------------------
#             GET SINGLE (200 OK)
# -----------------------------------------
@router.get(
    "/{expense_id}", response_model=StandardResponse, status_code=status.HTTP_200_OK
)
def get_single_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = crud.get_expense(db, expense_id)
    if not expense:
        return JSONResponse(
            status_code=404,
            content=StandardResponse(
                success=False,
                message="Expense not found",
                data=None,
                errors=[]
            ).model_dump()
        )

    return StandardResponse(
        success=True,
        message="Expense fetched successfully",
        data=expense,
    )


# -----------------------------------------
#            UPDATE (200 OK)
# -----------------------------------------
@router.patch(
    "/{expense_id}", response_model=StandardResponse, status_code=status.HTTP_200_OK
)
def update_expense_route(
    expense_id: int,
    expense: schemas.ExpenseUpdate,
    db: Session = Depends(get_db),
):
    updated = crud.update_expense(db, expense_id, expense)
    if not updated:
        return JSONResponse(
            status_code=404,
            content=StandardResponse(
                success=False,
                message="Expense not found",
                data=None,
                errors=[]
            ).model_dump()
        )

    return StandardResponse(
        success=True,
        message="Expense updated successfully",
        data=updated,
    )


# -----------------------------------------
#        DELETE (200 OK)
# -----------------------------------------
@router.delete("/{expense_id}", response_model=StandardResponse, status_code=status.HTTP_200_OK)
def delete_expense_route(expense_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_expense(db, expense_id)
    if not deleted:
        return JSONResponse(
            status_code=404,
            content=StandardResponse(
                success=False,
                message="Expense not found",
                data=None,
                errors=[]
            ).model_dump()
        )

    return StandardResponse(
        success=True,
        message="Expense deleted successfully",
        data=[]
    )
