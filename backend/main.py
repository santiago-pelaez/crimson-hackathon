### This is the file where the front end and the back end are connected. Ts is hte main file of the backend and controls the enter application DO NOT TOUCH #####

########## IMPORTS ##########
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json
import threading
import os
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv
from pathlib import Path
import re
from fastapi.middleware.cors import CORSMiddleware

# agentic ai type shiitititii
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import SystemMessage, HumanMessage
except Exception:
    print("There was an error importing the langchain_google_genai package.")
    ChatGoogleGenerativeAI = None
########## END OF IMPORTS ##########

########## SETUP ##########
# Load .env from repo if available (more flexible)
env_path = Path(__file__).resolve().parent / ".env"
if not env_path.exists():
    env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(str(env_path))
else:
    load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
# Debug print: show if key is loaded (first 5 chars)
if gemini_api_key:
    print(f"DEBUG: API Key Loaded: {gemini_api_key[:5]}*****")
else:
    print("DEBUG: GEMINI_API_KEY not set. AI features will be disabled.")

GEMINI_MODEL = "gemini-2.5-flash"
LOG_FILE = os.path.join(os.path.dirname(__file__), "logs.json")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

_state_lock = threading.Lock()
####### End of establishing base variables #######

system_state = {
    "is_locked": False,
    "threat_level": 0,
    "ai_thoughts": ["Sentry active. Monitoring network traffic..."],
    "queue_status": "Green",
    "pending_approvals": [],
    "user_data": {}
}

def _read_logs(max_lines: int = 100) -> List[Dict]:
    if not os.path.exists(LOG_FILE): return []
    entries = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries[-max_lines:]

def run_security_check(current_user: str, metadata: dict) -> Dict:
    logs = _read_logs(50)
    log_snippet = json.dumps(logs, indent=2)

    with _state_lock:
        if current_user not in system_state["user_data"]:
            system_state["user_data"][current_user] = {"score": 0, "attempts": 0}

        user = system_state["user_data"][current_user]

        if metadata.get("status") == "failed":
            user["attempts"] += 1
            user["score"] += 15

    # AI prompt with structured format
    prompt = f"""
    You are the Aegis Heuristic Sentry. Analyze the login attempt and recent logs.
    STRICT OUTPUT FORMAT (single line, no explanation):
    VERDICT: [GREEN/YELLOW/RED] | SCORE: [0-100] | REASON: [Max 15 words explanation]

    Login user: {current_user}
    Metadata: {json.dumps(metadata)}
    Recent Logs: {log_snippet}
    """

    def _parse_sentry_output(text: str) -> Dict:
        out = {"verdict": "GREEN", "score": 0, "reason": "No reason provided."}
        if not text: return out
        m = re.search(r"VERDICT:\s*([A-Za-z]+)\s*\|\s*SCORE:\s*(\d{1,3})\s*\|\s*REASON:\s*(.+)", text, flags=re.IGNORECASE)
        if m:
            verdict = m.group(1).upper().strip()
            try:
                score = int(re.sub(r"[^0-9]", "", m.group(2)))
            except:
                score = 0
            reason = " ".join(m.group(3).strip().split()[:15])
            return {"verdict": verdict, "score": max(0, min(100, score)), "reason": reason}
        return out

    try:
        if not ChatGoogleGenerativeAI or not gemini_api_key:
            raise RuntimeError("AI Configuration Missing")

        model = ChatGoogleGenerativeAI(
            google_api_key=gemini_api_key,
            model=GEMINI_MODEL,
            temperature=0
        )
        resp = model.invoke([SystemMessage(content="You are Aegis Heuristic Sentry."), HumanMessage(content=prompt)])
        parsed = _parse_sentry_output(str(resp.content))

    except Exception as e:
        print(f"CRITICAL: AI SENTRY OFFLINE - {str(e)}")
        parsed = {
            "verdict": ("RED" if user.get("score", 0) >= 60 else "GREEN"),
            "score": user.get("score", 0),
            "reason": "Autonomous mode: score-based triage."
        }

    with _state_lock:
        system_state["queue_status"] = parsed["verdict"].title()
        system_state["threat_level"] = parsed["score"]
        system_state["ai_thoughts"] = [parsed["reason"]]
        if parsed["verdict"] == "RED":
            system_state["is_locked"] = True
        if parsed["verdict"] == "YELLOW" and metadata.get("status") == "success":
            system_state["pending_approvals"].append({
                "user": current_user,
                "time": datetime.now().strftime("%H:%M:%S")
            })

    return parsed

@app.get("/status")
def get_status():
    """This is what the Frontend polls every 1 second to see if it should blur."""
    with _state_lock: return system_state

@app.post("/log-event")
async def log_event(data: dict):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    analysis = run_security_check(data.get("username", "unknown"), data)
    return {
        "status": "processed",
        "analysis_result": {
            "summary": analysis.get("reason"),
            "details": {"verdict": analysis.get("verdict"), "score": analysis.get("score")}
        }
    }

@app.post("/unlock")
def unlock_system():
    with _state_lock:
        system_state.update({
            "is_locked": False,
            "threat_level": 0,
            "queue_status": "Green",
            "ai_thoughts": ["System Reset."],
            "user_data": {},
            "pending_approvals": []
        })
    return {"message": "Unlocked"}

@app.post("/lock")
def manual_lock():
    with _state_lock:
        system_state["is_locked"] = True
        system_state["threat_level"] = 85
        system_state["ai_thoughts"] = ["Manual lock triggered for demo"]
    return {"status": "locked"}

########## CHAT & LOGS ENDPOINTS ##########

class ChatRequest(BaseModel):
    message: str
    context: list

@app.get("/logs")
def get_logs():
    return _read_logs(100)

@app.post("/chat")
async def chat_with_gemini(request: ChatRequest):
    if not ChatGoogleGenerativeAI or not gemini_api_key:
        return {"response": "AI Module not loaded."}

    try:
        log_context = json.dumps(request.context[-10:], indent=2)
        prompt = f"""
        You are the Aegis Cyber Advisor. Answer the user question professionally and concisely. Max 3 sentences.
        Recent Security Logs: {log_context}
        User Question: {request.message}
        """

        model = ChatGoogleGenerativeAI(
            google_api_key=gemini_api_key,
            model=GEMINI_MODEL,
            temperature=0.7
        )
        resp = model.invoke([SystemMessage(content="You are the Aegis Cyber Advisor."), HumanMessage(content=prompt)])
        return {"response": str(resp.content)}
    except Exception as e:
        return {"response": f"Advisor Error: {str(e)}"}
