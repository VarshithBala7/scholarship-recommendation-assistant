from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    academic_level = Column(String(50), nullable=False)  # e.g., high_school, undergrad
    major = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    gpa = Column(String(10), nullable=True)
    goals = Column(Text, nullable=True)

    queries = relationship("ScholarshipQuery", back_populates="user")


class ScholarshipQuery(Base):
    __tablename__ = "scholarship_queries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    raw_input = Column(Text, nullable=False)
    llm_model = Column(String(50), nullable=False)
    llm_prompt = Column(Text, nullable=False)
    llm_response_raw = Column(Text, nullable=False)
    llm_response_structured = Column(JSON, nullable=False)
    token_usage_prompt = Column(Integer, nullable=True)
    token_usage_completion = Column(Integer, nullable=True)
    token_usage_total = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("UserProfile", back_populates="queries")
