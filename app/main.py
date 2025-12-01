from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from . import models, database
from .routes import expenses

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Expense Tracker API", version="2.0")

# Register routes
app.include_router(expenses.router)


# -----------------------------------
#   ADVANCED VALIDATION ERROR HANDLER
# -----------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    error_list = []

    for err in exc.errors():
        field = err["loc"][-1]  # last element of "loc" is the field name
        error_type = err["type"]
        message = err["msg"]

        # Missing required field
        if error_type == "missing":
            error_list.append(
                {
                    "field": field,
                    "error": "missing",
                    "message": f"The '{field}' field is required.",
                }
            )

        # Wrong type or invalid type
        elif "type_error" in error_type or "date_from_datetime" in error_type:
            error_list.append(
                {
                    "field": field,
                    "error": "invalid_type",
                    "message": f"The '{field}' field has an invalid type.",
                }
            )

        # Other invalid values
        else:
            error_list.append(
                {
                    "field": field,
                    "error": "invalid_value",
                    "message": message,
                }
            )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation error",
            "data": None,
            "errors": error_list,
        },
    )


# Home Route
@app.get("/")
def home():
    return {"message": "FastAPI + MySQL Expense Tracker is running 🚀"}
