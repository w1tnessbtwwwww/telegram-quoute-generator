

from typing import Generic, TypeVar, Optional

T = TypeVar('T')


class Result(Generic[T]):
    def __init__(self, 
                 success: bool, 
                 value: Optional[T] = None, 
                 error: Optional[str] = None):
        self.success = success
        self.value = value
        self.error = error

def err(msg: Optional[str]) -> Result[None]: return Result(success=False, error=msg)

def success(value: Optional[T]) -> Result[T]: return Result(success=True, value=value)