from pydantic import BaseModel
from typing import Any
from datetime import date

class Application(BaseModel):
    startDate: date
    endDate: date
    type: str
    purpose: Any = None
    days: int
    applicationDate: date

class ApplicationResponse(BaseModel):
    response: int
    applicationData: date
