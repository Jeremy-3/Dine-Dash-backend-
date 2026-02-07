# app/main.py
from fastapi import FastAPI,APIRouter,Request,Depends,Response
from fastapi.middleware.cors import CORSMiddleware
from app.handlers import exception_handlers
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.lifespan import app_lifespan
from sqlalchemy.exc import SQLAlchemyError


app = FastAPI(
    title="Dine and Dash API Service",
    version="1.0.0",
    redoc_url=False,
    lifespan=app_lifespan,
    contact={
        "name": "D&D support",
        "email": "jeremyhizashi@gmail.com",
    }
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register exception handlers
app.add_exception_handler(StarletteHTTPException, exception_handlers.http_exception_handler)
app.add_exception_handler(RequestValidationError, exception_handlers.validation_exception_handler)
app.add_exception_handler(Exception, exception_handlers.generic_exception_handler)
app.add_exception_handler(SQLAlchemyError, exception_handlers.sqlalchemy_exception_handler)


# Include all routers
api_router = APIRouter(prefix="/api")

app.include_router(api_router) # include main router in the app





