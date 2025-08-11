import json
import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

DATA_FILE = "style_sample.json"

def load_all_samples():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_all_samples(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def save_style_samples(user_id: str, answers: dict):
    all_samples = load_all_samples()
    all_samples[user_id] = answers
    save_all_samples(all_samples)

def load_style_samples(user_id: str) -> dict:
    all_samples = load_all_samples()
    return all_samples.get(user_id, {})

    
router = APIRouter()

QUESTIONS = [
    "Describe how your ideal day feels, in your own words.",
    "Write a sentence or two about how you handle tough moments.",
    "What’s something you’d say to yourself when you want to focus?"
]

# In-memory storage example — replace with your DB or file system
user_style_samples_store: Dict[str, Dict[str, str]] = {}

class StyleSamples(BaseModel):
    ideal_day: str
    tough_moments: str
    focus_phrase: str

@router.get("/onboarding/questions")
async def get_questions():
    return {"questions": QUESTIONS}

@router.post("/onboarding/style-samples/{user_id}")
async def save_style_samples(user_id: str, samples: StyleSamples):
    user_style_samples_store[user_id] = samples.dict()
    return {"status": "success", "message": f"Style samples saved for user {user_id}"}

@router.get("/onboarding/style-samples/{user_id}")
async def load_style_samples(user_id: str):
    samples = user_style_samples_store.get(user_id)
    if not samples:
        raise HTTPException(status_code=404, detail="Style samples not found")
    return samples