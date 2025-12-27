# Scholarship Recommendation Assistant (Demo)

This repository contains a minimal backend for a **Scholarship Recommendation Assistant**.

It demonstrates:

- A student **profile** model
- A **scholarship query** endpoint
- A database schema for **storing queries and structured recommendations**
- A (demo) LLM-like response that returns scholarship recommendations as **structured JSON**

## Tech Stack

- Python, FastAPI
- SQLite via SQLAlchemy
- Pydantic schemas

## How It Works

1. Create a user (student profile) via `POST /users/`.
2. Submit a scholarship query via `POST /scholarships/query`.
3. The API builds a prompt (profile + query), calls a simulated LLM, and
   stores:
   - Raw input
   - Prompt text
   - Raw LLM response
   - Structured JSON with scholarship recommendations
4. You can list past queries for a user via `GET /scholarships/user/{user_id}`.

> Note: For simplicity and portability on GitHub, this project uses a **fake LLM response**
> so it runs without API keys. It still demonstrates how to integrate LLM output with
> a SQL-backed database and structured JSON responses.
