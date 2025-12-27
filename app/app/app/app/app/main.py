import os
import json
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import schemas, crud, prompts, models

# For this GitHub demo, we won't actually call OpenAI.
# We'll fake an LLM response so the project runs without keys.


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Scholarship Recommendation Assistant (Demo)")


@app.post("/users/", response_model=schemas.UserProfileOut)
def create_user(user: schemas.UserProfileCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, email=user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@app.get("/users/{user_id}", response_model=schemas.UserProfileOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/scholarships/query", response_model=schemas.ScholarshipQueryOut)
def query_scholarships(payload: schemas.ScholarshipQueryCreate, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile_text = (
        f"Name: {user.name}\n"
        f"Academic level: {user.academic_level}\n"
        f"Major: {user.major}\n"
        f"Location: {user.location}\n"
        f"GPA: {user.gpa}\n"
        f"Goals: {user.goals}\n"
    )

    prompt = prompts.BASE_PROMPT + "\n\n" + \
        "STUDENT PROFILE:\n" + profile_text + \
        "\nSTUDENT QUERY:\n" + payload.raw_input

    # --- FAKE LLM RESPONSE FOR DEMO PURPOSES ---
    fake_structured = [
        {
            "name": "Example Data Science Scholarship",
            "provider": "Demo Foundation",
            "amount": "$5,000",
            "deadline": "2025-12-31",
            "url": "https://example.org/scholarship",
            "match_reason": "Matches student's interest in data science and academic performance.",
        }
    ]
    message_content = json.dumps(fake_structured, indent=2)

    usage = {
        "prompt_tokens": None,
        "completion_tokens": None,
        "total_tokens": None,
    }

    db_query = crud.create_scholarship_query(
        db=db,
        user_id=user.id,
        raw_input=payload.raw_input,
        llm_model="demo-llm",
        prompt=prompt,
        response_raw=message_content,
        response_structured=fake_structured,
        token_usage=usage,
    )

    return db_query


@app.get("/scholarships/user/{user_id}", response_model=list[schemas.ScholarshipQueryOut])
def list_scholarship_queries(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    queries = crud.list_queries_for_user(db, user_id=user_id)
    return queries
