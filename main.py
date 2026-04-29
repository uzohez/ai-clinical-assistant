from fastapi import FastAPI
from pydantic import BaseModel
from triage_engine import run_triage
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

class PatientInput(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
def chat(data: PatientInput):
    response = run_triage(data.session_id, data.message)
    return response