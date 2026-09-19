from pydantic import BaseModel

class TimeTable(BaseModel):
    empId: str
    periods: dict[str, list[str]]
