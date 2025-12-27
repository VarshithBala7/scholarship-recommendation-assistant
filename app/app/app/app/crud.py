from sqlalchemy.orm import Session
from . import models, schemas


def create_user(db: Session, user: schemas.UserProfileCreate) -> models.UserProfile:
    db_user = models.UserProfile(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.UserProfile).filter(models.UserProfile.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.UserProfile).filter(models.UserProfile.email == email).first()


def create_scholarship_query(
    db: Session,
    user_id: int,
    raw_input: str,
    llm_model: str,
    prompt: str,
    response_raw: str,
    response_structured,
    token_usage: dict | None = None,
):
    db_query = models.ScholarshipQuery(
        user_id=user_id,
        raw_input=raw_input,
        llm_model=llm_model,
        llm_prompt=prompt,
        llm_response_raw=response_raw,
        llm_response_structured=response_structured,
        token_usage_prompt=token_usage.get("prompt_tokens") if token_usage else None,
        token_usage_completion=token_usage.get("completion_tokens") if token_usage else None,
        token_usage_total=token_usage.get("total_tokens") if token_usage else None,
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query


def list_queries_for_user(db: Session, user_id: int):
    return (
        db.query(models.ScholarshipQuery)
        .filter(models.ScholarshipQuery.user_id == user_id)
        .order_by(models.ScholarshipQuery.created_at.desc())
        .all()
    )
