from pydantic import BaseModel, EmailStr
from typing import Optional, Any, List


class UserProfileCreate(BaseModel):
    name: str
    email: EmailStr
    academic_level: str
    major: Optional[str] = None
    location: Optional[str] = None
    gpa: Optional[str] = None
    goals: Optional[str] = None


class UserProfileOut(UserProfileCreate):
    id: int

    class Config:
        orm_mode = True


class ScholarshipRecommendation(BaseModel):
    name: str
    provider: Optional[str] = None
    amount: Optional[str] = None
    deadline: Optional[str] = None
    url: Optional[str] = None
    match_reason: Optional[str] = None


class ScholarshipQueryCreate(BaseModel):
    user_id: int
    raw_input: str


class ScholarshipQueryOut(BaseModel):
    id: int
    user: UserProfileOut
    raw_input: str
    llm_model: str
    llm_response_structured: Any

    class Config:
        orm_mode = True
