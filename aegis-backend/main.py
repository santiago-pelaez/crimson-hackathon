### This is the file where the front end and the back end are connected. Ts is hte main file of the backend and controls the enter application DO NOT TOUCH #####



########## IMPORTS ##########
from fastapi import FastAPI
from pydantic import BaseModel
import json
import threading
from datetime import datetime
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv


try:
    from langchain_google_genai import GoogleGenerativeAI
except Exception:
    print("Error importing langchain_google_genai. Please make sure you have the correct version of langchain installed.")
    GoogleGenerativeAI = None

try:
    from crewai import Agent, Task, Crew, Process
except Exception:
    print("Error importing crewai. Please make sure you have the correct version of crewai installed.")
    Agent = None
    Task = None
    Crew = None
    Process = None

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
    
    with open(LOG_FILE, "r", encoding="uft-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return entries[-max_lines:]
    

def run_sucurity_check(timeout_seconds: int = 30)




# Define a Pydantic model for the system state 
@app.get("/status")
def get_system_status():
    return system_state


@app.post("/login-attempt")
def login_attempt(data: dict):
    # it should save the data to a json file
    with open("logs.json", "a") as f:
        f.write(json.dumps(data) + "\n")

        # run_ai_analysis(data) # this is a function that will run the ai analysis on the data and return the results
        # it should also update the system state based on the data to determine if there is a threat
        return {"message": "logged"}
    
@app.post("/unlock")
def unlock_system():
    system_state["is_locked"] = False
    system_state["threat_level"] = 0
    system_state["ai_thoughts"] = "System reset maunally. System is unlocked."
    return {"message": "System unlocked"}