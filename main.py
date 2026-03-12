# app/main.py
from fastapi import FastAPI,APIRouter,Request,Depends,Response
from fastapi.middleware.cors import CORSMiddleware
from app.handlers import exception_handlers
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
# from app.core.lifespan import app_lifespan
from sqlalchemy.exc import SQLAlchemyError

from app.routes import user, roles, permissions, role_permissions, address, restaurants, foods, orders, order_item, payments, deliveries, order_status_history , driver , auth



app = FastAPI(
    title="Dine and Dash API Service",
    version="1.0.0",
    redoc_url=False,
    contact={
        "name": "D&D support",
        "email": "jeremyhizashi@gmail.com",
    }
)
# @app.on_event("startup")
# def startup_event():
#     routes = []
#     for route in app.routes:
#         if hasattr(route, 'path'):
#             routes.append(f"{route.methods} {route.path}")
#     print("\n🚀 Registered Routes:")
#     for route in sorted(routes):
#         print(f"  {route}")


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

api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(roles.router)
api_router.include_router(permissions.router)
api_router.include_router(role_permissions.router)
api_router.include_router(address.router)
api_router.include_router(restaurants.router)
api_router.include_router(foods.router)
api_router.include_router(orders.router)
api_router.include_router(order_item.router)
api_router.include_router(payments.router)
api_router.include_router(deliveries.router)
api_router.include_router(order_status_history.router)
api_router.include_router(driver.router)




app.include_router(api_router) # include main router in the app





