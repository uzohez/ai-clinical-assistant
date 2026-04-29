import os
from openai import OpenAI
from dotenv import load_dotenv
from database import SessionLocal
from models import Conversation
from risk_model import get_risk_level

from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a clinical assistant AI.

Return structured output:

{
  "follow_up_questions": [],
  "possible_conditions": [],
  "recommendations": []
}
"""

def run_triage(session_id, user_input):
    db = SessionLocal()

    # fetch history
    history = db.query(Conversation).filter(Conversation.session_id == session_id).all()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})

    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"AI error: {str(e)}"

    # save conversation
    db.add(Conversation(session_id=session_id, role="user", content=user_input))
    db.add(Conversation(session_id=session_id, role="assistant", content=reply))
    db.commit()

    risk = get_risk_level(user_input)

    return {
        "response": reply,
        "risk_level": risk
    }