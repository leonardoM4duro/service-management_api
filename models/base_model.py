from beanie import Document
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BaseEntity(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    disabled: bool