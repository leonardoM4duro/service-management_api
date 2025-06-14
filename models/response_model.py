from typing import Any, Optional
from pydantic import BaseModel

class ResponseModel(BaseModel):
    success: bool = True
    data: Optional[Any] = None
    error: Optional[str] = None

    @classmethod
    def build(cls, success: bool = True, data: Any = None, error: str = None):
        if error:
            return cls(success=False, data=None, error=error)
        return cls(success=success, data=data, error=None)
