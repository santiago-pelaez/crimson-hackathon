########## IMPORTS ##########
from fastapi import FastAPI
from pydantic import BaseModel, Field
import json
import threading
import os
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import SystemMessage, HumanMessage
except Exception:
    ChatGoogleGenerativeAI = None

########## SETUP ##########
load_dotenv(r"C:\Users\chika\OneDrive\Documents\crimson-hackathon\aegis-backend\.env")
gemini_api_key = os.getenv("GEMINI_API_KEY")
print(f"DEBUG: API Key Loaded: {gemini_api_key[:5]}*****")
GEMINI_MODEL = "gemini-2.5-flash"
LOG_FILE = os.path.join(os.path.dirname(__file__), "logs.json")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

_state_lock = threading.Lock()

# New State Structure based on your requirements
system_state = {
    "is_locked": False,
    "threat_level": 0,
    "queue_status": "Green", 
    "ai_thoughts": ["Sentry active. Monitoring network traffic..."],
    "pending_approvals": [], # Users in Yellow Queue
    "user_data": {} # Tracks scores and attempts: { "username": {"score": 0, "attempts": 0} }
}

def _read_logs(max_lines: int = 100) -> List[Dict]:
    if not os.path.exists(LOG_FILE): return []
    entries = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try: entries.append(json.loads(line))
            except: continue
    return entries[-max_lines:]

def run_security_check(current_user: str, metadata: dict) -> Dict:
    logs = _read_logs(50)
    log_snippet = json.dumps(logs, indent=2)
    
    with _state_lock:
        # Initialize user if new
        if current_user not in system_state["user_data"]:
            system_state["user_data"][current_user] = {"score": 0, "attempts": 0}
        
        user = system_state["user_data"][current_user]
        
        # LOGIC: Points for failed attempts
        if metadata.get("status") == "failed":
            user["attempts"] += 1
            user["score"] += 15 # Each failure = 15 points
        
    # AI AGENTIC CLASSIFICATION
    prompt = f"""
    Analyze this login attempt for user: {current_user}
    Metadata: {json.dumps(metadata)}
    Recent Logs: {log_snippet}

    RULES:
    1. GREEN: (Score <= 30) Domestic/West Coast.
    2. YELLOW: (Score < 60) Domestic VPN or Suspicious activity.
    3. RED: (Score >= 60 or Non-U.S. IP). Brute force detected.

    Provide a verdict in this format:
    VERDICT: [GREEN/YELLOW/RED]
    REASON: [Short professional explanation]
    """

    try:
        model = ChatGoogleGenerativeAI(api_key=gemini_api_key, model=GEMINI_MODEL, temperature=0)
        resp = model.invoke([SystemMessage(content="You are Aegis Sentry Security."), HumanMessage(content=prompt)])
        ai_res = str(resp.content)
        
        # Parse AI Decision
        new_queue = "Green"
        if "RED" in ai_res.upper(): new_queue = "Red"
        elif "YELLOW" in ai_res.upper(): new_queue = "Yellow"
        
        reason = ai_res.split("REASON:")[-1].strip() if "REASON:" in ai_res else ai_res

    except Exception as e:
        print(f"AI Error: {e}")
        new_queue = "Red" if user["score"] >= 60 else "Green"
        reason = "Autonomous mode active. Score-based Triage."

    with _state_lock:
        system_state["queue_status"] = new_queue
        system_state["threat_level"] = user["score"]
        system_state["ai_thoughts"] = [reason]
        
        # RED triggers Lockdown
        if new_queue == "Red":
            system_state["threat_level"] = 100 
            system_state["is_locked"] = True
        else:
            system_state["threat_level"] = user["score"]
            
        system_state["ai_thoughts"] = [reason]
        
        # YELLOW triggers Manual Review
        if new_queue == "Yellow" and metadata.get("status") == "success":
            system_state["pending_approvals"].append({"user": current_user, "time": datetime.now().strftime("%H:%M:%S")})

    return {"queue": new_queue, "score": user["score"]}

@app.get("/status")
def get_status():
    with _state_lock: return system_state

@app.post("/log-event")
async def log_event(data: dict):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    
    analysis = run_security_check(data.get("username", "unknown"), data)
    return {"status": "processed", "analysis": analysis}

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

########## CHAT & LOGS ENDPOINTS ##########

class ChatRequest(BaseModel):
    message: str
    context: list

@app.get("/logs")
def get_logs():
    # This reads your existing LOG_FILE and returns it as a list for the table
    return _read_logs(100)

@app.post("/chat")
async def chat_with_gemini(request: ChatRequest):
    if not ChatGoogleGenerativeAI:
        return {"response": "AI Module not loaded. Check dependencies."}
    
    try:
        # Create a prompt that includes the security logs as context
        log_context = json.dumps(request.context[-10:], indent=2)
        prompt = f"""
        You are the Aegis Sentry AI. 
        Recent Security Logs: {log_context}
        User Question: {request.message}
        
        Provide a concise, professional security analysis or answer based on the logs provided.
        """
        
        model = ChatGoogleGenerativeAI(api_key=gemini_api_key, model=GEMINI_MODEL, temperature=0.7)
        resp = model.invoke([SystemMessage(content="You are Aegis Sentry Intelligence Hub."), HumanMessage(content=prompt)])
        
        return {"response": str(resp.content)}
    except Exception as e:
        return {"response": f"Gemini Error: {str(e)}"}