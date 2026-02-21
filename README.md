# Aegis Labyrinth (OLED Edition)
**Reinvent the firewall into a physical, agentic guardian.**

Aegis Labyrinth is a hackathon MVP that combines:
- **Selective Freeze**: only sensitive admin actions “lock”
- **Deception (Labyrinth honeypot)**: suspicious users get routed into a decoy admin panel
- **Physical authorization**: a **real button** on a Raspberry Pi unlocks the admin vault
- **Hardware visibility**: a **small OLED** displays threat level + state in real time
- **Optional agentic AI**: CrewAI/LLM generates explanations & incident reports

Theme: **REINVENT THE WHEEL**  
We reinvent a static firewall “wall” into a **maze** with a **physical deadlock** that can’t be bypassed remotely.

---

## What you can demo in 2 minutes
### 1) Customer View (`/`)
A simple storefront page (e.g., “Mom’s Bakery”). This **never locks**.

### 2) Admin View (`/admin`)
Admin has sensitive actions (fake but realistic):
- Export data
- Delete user
- Update pricing

When a suspicious scenario is detected, the system triggers a **Vault Freeze**:
- React admin shows a premium blur overlay: “Physical Auth Required”
- OLED shows `LOCKED` + `Threat: XX/100`
- Pressing the **physical button** unlocks for a short window (e.g., 60 seconds)

### 3) Labyrinth honeypot (`/labyrinth/admin`)
Suspicious users are redirected to a decoy admin panel that:
- looks real
- logs everything
- never touches real data

---

## Hardware (minimum)
You already have: Raspberry Pi, power supply, microSD, breadboard, USB→Ethernet.

You still need:
- **I2C OLED display** (recommended: SSD1306 128×64, 0.96")
- **Momentary push button** (tactile)
- **Dupont jumper wires** (female↔female + female↔male, depending on OLED pins)
- Optional: **LED + 220–330Ω resistor** for ambient status
- (Bring-up recommended) microSD reader + HDMI/keyboard for initial setup

---

## Software components
### Backend (FastAPI, Python)
Single source of truth for:
- `locked` state (vault frozen?)
- `threat_level` (0–100)
- `unlocked_until` timestamp (physical unlock window)
- event logs

Suggested endpoints:
- `GET /api/status`
- `POST /api/lock`
- `POST /api/unlock` (called by the Pi button)
- `GET /api/logs`
- `POST /api/reset` (demo helper)

### Frontend (React + Tailwind)
- `/` storefront route
- `/admin` admin route
- polls `/api/status` every 1s
- shows lock overlay when `locked=true`

### Hardware daemon (Python on the Pi)
- polls `/api/status`
- updates OLED display (SAFE / INVESTIGATING / LOCKED + threat)
- on button press → `POST /api/unlock`

### Optional AI (CrewAI/LLM)
- reads recent events
- generates a short “incident autopsy” report
- must have a fallback if AI is slow/unavailable

---

## Where to start
Read the build plan: **[ROADMAP.md](ROADMAP.md)**

---

## Safety / Ethics
- Demo on a local network you control.
- Do not collect real credentials.
- Honeypot is for demonstration/education only.
