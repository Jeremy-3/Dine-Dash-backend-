from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, Any
from pydantic.generics import GenericModel

T = TypeVar("T")

class ResponseModel(GenericModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: Optional[str] = "Operation Successful"
    errors: Optional[Any] = None
    total: Optional[int] = None
