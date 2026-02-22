### This is the file where the front end and the back end are connected. Ts is hte main file of the backend and controls the enter application DO NOT TOUCH #####



########## IMPORTS ##########
from fastapi import FastAPI
from pydantic import BaseModel, Field # Added Field here
import json
import threading
from datetime import datetime
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

# agentic ai type shiitititii
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import SystemMessage, HumanMessage
except Exception:
    print("There was an error importing the langchain_google_genai package.")
    ChatGoogleGenerativeAI = None
########## END OF IMPORTS ##########


####### Establishing varibles etc. #######

load_dotenv() 
gemini_api_key = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL ="gemini-2.5-flash" 
LOG_FILE = os.path.join(os.path.dirname(__file__), "logs.json")

app = FastAPI()

_state_lock = threading.Lock()
####### ENd of establishing base varibles #######




#pydantic data
system_state = {
    "is_locked": False,
    "threat_level": 0,
    "ai_thoughts": "System monitoring for threats . . . . . . ",
}

def _read_logs(max_lines: int = 200) -> List[Dict]:
    if not os.path.exists(LOG_FILE):
        return []
    entries: List[Dict] = []
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
    

class SecurityAnalysis(BaseModel):
    detected_hack: bool = Field(description="Whether a security threat was found")
    summary: str = Field(description="Short summary of the analysis")


def run_security_check(timeout_seconds: int = 15) -> Dict:
    logs = _read_logs(200)
    snippet = json.dumps(logs[-100:], ensure_ascii=False, indent=2)

    MAX_CHARS = 12000
    if len(snippet) > MAX_CHARS:
        snippet = snippet[-MAX_CHARS:]

    detected = False
    summary = "Analysis failed."

    if not gemini_api_key or not ChatGoogleGenerativeAI:
        summary = "AI not configured; using heuristic fallback."
    else:
        try:
            # Initializes model
            model = ChatGoogleGenerativeAI(api_key=gemini_api_key, model=GEMINI_MODEL, temperature=0)

            # 1. Attemp: the structered output
            try:
                structured = model.with_structured_output(SecurityAnalysis)
                result = structured.invoke([
                    SystemMessage(content="You are a security sentry. Return JSON {detected_hack,summary}."),
                    HumanMessage(content=f"Analyze these recent logs:\n\n{snippet}")
                ])
                
                detected = bool(result.detected_hack)
                summary = str(result.summary)
            except Exception:
                # Plan B: Fallback to plain text if structured fails
                resp = model.invoke([
                    SystemMessage(content="You are a security sentry. Respond in plain text."),
                    HumanMessage(content=f"Is there a hack in these logs? Summarize: {snippet}")
                ])
                summary = str(resp.content)
                detected = any(k in summary.lower() for k in ("hack", "breach", "unauthorized", "intrusion"))

        except Exception as e:
            summary = f"Eerrr ai call: {type(e).__name__}; using the fallback sys."

    # lil satfty net
    if "fallback" in summary or summary == "Analysis failed.":
        lower = snippet.lower()
        heuristics = ("failed login", "brute force", "unauthorized", "compromised", "hack")
        detected = any(h in lower for h in heuristics)
        summary = "(Using fallback) threat detected: . . . " if detected else "(Using Fallback): no threats found"

    with _state_lock:
        if detected:
            system_state["is_locked"] = True
            system_state["threat_level"] = max(1, system_state.get("threat_level", 0) + 1)
        system_state["ai_thoughts"] = summary

    return {"detected_hack": bool(detected), "summary": summary}

@app.get("/status")
def get_status():
    """This is what the Frontend polls every 1 second to see if it should blur."""
    with _state_lock:
        return system_state

@app.post("/login-attempt")
def login_attempt(data: Dict):
    # 1. Save log
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    
    # 2. TRIGGER THE AI 
    # We run the check every time someone tries to login
    analysis = run_security_check()
    
    return {
        "message": "logged",
        "analysis_result": analysis
    }

@app.post("/unlock")
def unlock_system():
    with _state_lock:
        system_state["is_locked"] = False
        system_state["threat_level"] = 0
        system_state["ai_thoughts"] = "System reset manually. System is unlocked."
    return {"message": "System unlocked"}

@app.post("/lock")
def manual_lock():
    with _state_lock:
        system_state["is_locked"] = True
        system_state["threat_level"] = 85
        system_state["ai_thoughts"] = "Manual lock triggered for demo"
    return {"status": "locked"}

# --- TO RUN THE SERVER ---
# Type to terminal:
# uvicorn main:app --reload