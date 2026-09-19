from typing import Optional
from pydantic import BaseModel

class SignIn(BaseModel):
    email: str
    password: str
    role: str

class Signup(BaseModel):
    email: str
    pws: str
    id: Optional[str] = None
    name: Optional[str] = None
    role: str = "employee"
    designation: Optional[str] = None
    photo: Optional[str] = None
    department: Optional[str] = None
    joiningDate: Optional[str] = None
