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

# Replace the old load_dotenv() with this:
load_dotenv(r"C:\Users\chika\OneDrive\Documents\crimson-hackathon\aegis-backend\.env")

gemini_api_key = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL ="gemini-2.5-flash" 
LOG_FILE = os.path.join(os.path.dirname(__file__), "logs.json")

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your React app to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_state_lock = threading.Lock()
####### ENd of establishing base varibles #######




#pydantic data
system_state = {
    "is_locked": False,
    "threat_score": 0,
    "queue_status": "Green", # Green, Yellow, Red
    "ai_thoughts": "System monitoring...",
    "pending_approvals": [] # For your manual review feature
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
    logs = _read_logs(100)
    snippet = json.dumps(logs, ensure_ascii=False, indent=2)

    if not gemini_api_key or not ChatGoogleGenerativeAI:
        return {"detected_hack": False, "summary": "AI Configuration Error"}

    try:
        model = ChatGoogleGenerativeAI(api_key=gemini_api_key, model=GEMINI_MODEL, temperature=0)

        # Simplified prompt: Ask for a specific prefix to determine the lock status
        resp = model.invoke([
            SystemMessage(content="""You are Aegis Sentry, an elite cybersecurity AI. 
            Analyze the logs for patterns like brute force or suspicious IPs. 
            If you find a threat and want to lock the system, start your response with 'VERDICT: LOCK'. 
            Otherwise, start with 'VERDICT: SAFE'. 
            Then provide a concise summary."""),
            HumanMessage(content=f"Analyze these logs:\n\n{snippet}")
        ])
        
        raw_text = str(resp.content)
        summary = raw_text.replace("VERDICT: LOCK", "").replace("VERDICT: SAFE", "").strip()
        detected = "VERDICT: LOCK" in raw_text.upper()

    except Exception as e:
        print(f"AI Error: {e}")
        # Local Heuristic (This is your safety net, but it won't trigger 'Fallback' text anymore)
        lower = snippet.lower()
        detected = lower.count("failed") > 3 
        summary = "AI Link Interrupted. Heuristic analysis active."

    with _state_lock:
        if detected:
            system_state["is_locked"] = True
            # Level jumps to 100 on hack, or climbs
            system_state["threat_level"] = 100
        else:
            # Gradually lower threat level if things are safe
            system_state["threat_level"] = max(0, system_state["threat_level"] - 10)
            
        system_state["ai_thoughts"] = summary

    return {"detected_hack": bool(detected), "summary": summary}

@app.get("/status")
def get_status():
    """This is what the Frontend polls every 1 second to see if it should blur."""
    with _state_lock:
        return system_state

@app.post("/log-event")  # <--- Changed this from /login-attempt
async def log_event(data: dict):
    # 1. Save the JSON data to your log file
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    
    # 2. TRIGGER THE AI ANALYSIS
    # This calls run_security_check() which talks to Gemini
    analysis = run_security_check()
    
    print(f" Log received: {data['username']} - Status: {data['status']}")
    print(f" Gemini Analysis: {analysis['summary']}")
    
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