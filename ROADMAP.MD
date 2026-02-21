# Aegis Labyrinth — Implementation Roadmap (OLED + Button)
This roadmap is designed for a **24-hour hackathon**. The rule is: **build one working end-to-end loop early**, then add intelligence and polish.

---

## Key MVP loop (must work early)
**Backend locks → Admin overlay appears → OLED shows LOCKED → physical button unlocks → overlay disappears.**

If you accomplish only this + basic logs, you already have a strong demo.

---

## Decisions to lock (do these first)
1) OLED type: **I2C SSD1306 128×64** (recommended)
2) Networking: use **Ethernet** via USB→Ethernet, or a controlled hotspot/router
3) Unlock window: **60 seconds** (recommended)
4) Detection: start **rule-based**, add AI later
5) CrewAI: **stretch goal** unless you already know it well
6) Email: **stretch goal** (show report on dashboard first)

---

## Phase 0 — Hardware bring-up (Hour 0–1.5)
### Goal
Prove OLED + button works on the Pi.

### Tasks
- Flash Raspberry Pi OS to microSD
- Boot Pi, enable SSH
- Enable I2C (if OLED is I2C)
- Wire OLED (VCC, GND, SDA, SCL)
- Run an OLED “hello world”
- Wire button to GPIO (recommended: GPIO + GND with internal pull-up)
- Run a button test (prints when pressed)

### Checkpoint
- OLED displays text reliably
- Button press is detected reliably

> If this fails, fix it now. Don’t proceed until hardware is stable.

---

## Phase 1 — Skeleton end-to-end (Hours 1.5–4)
### Goal
Get the MVP loop working without AI or honeypot.

### Backend (FastAPI)
Implement in-memory state:
- `locked: bool`
- `threat_level: int`
- `unlocked_until: float | null`
- `events: list`

Endpoints:
- `GET /api/status`
- `POST /api/lock` (for testing)
- `POST /api/unlock` (sets `unlocked_until=now+60` and `locked=false`)
- `POST /api/reset`

### Frontend (React + Tailwind)
- Routes: `/` and `/admin`
- `/admin` polls `/api/status` every 1s
- Overlay component:
  - shown when `locked=true`
  - message: “Physical Auth Required. Press Aegis button.”

### Hardware daemon (Pi)
- Poll `GET /api/status` every 1s
- Render OLED:
  - `State: SAFE|LOCKED`
  - `Threat: XX/100`
  - `Press button to unlock` when locked
- On button press: `POST /api/unlock`

### Checkpoint
- Clicking “Lock” (or calling `/api/lock`) locks admin UI + OLED updates
- Pressing button unlocks within ~1 second

---

## Phase 2 — Admin actions + logging (Hours 4–7)
### Goal
Make the admin feel real and create an audit trail.

### Backend
- Add fake admin actions:
  - `POST /api/admin/export`
  - `POST /api/admin/delete-user`
  - `POST /api/admin/update-pricing`
- Log events for each action and request
- Add:
  - `GET /api/logs?limit=50`

### Frontend
- Admin page buttons that call those endpoints
- Live log feed in the admin page or a `/dashboard` page

### Checkpoint
- Buttons generate logs; logs appear live in UI

---

## Phase 3 — Selective Freeze policy (Hours 7–10)
### Goal
Only sensitive actions are blocked by the lock.

### Backend
- Implement “vault guard” on sensitive endpoints:
  - if locked and not within unlock window → return `403 PhysicalAuthRequired`
- Make `/admin` page itself viewable, but actions blocked when frozen

### Frontend
- If action returns 403 PhysicalAuthRequired:
  - show overlay
  - keep polling until unlocked

### Checkpoint
- Storefront always works
- Admin page loads
- Sensitive actions are blocked when locked

---

## Phase 4 — Labyrinth honeypot (Hours 10–14)
### Goal
Add deception: a decoy admin to trap suspicious users.

### Backend
- Add `/labyrinth/admin` routes:
  - fake login
  - fake dashboard
  - fake actions (export/delete)
- Log every honeypot interaction

### Routing rule (simple MVP)
- When `locked=true`, redirect suspicious flows from “real admin action” → labyrinth pages (or show a link)

### Checkpoint
- Attacker can interact with decoy
- Defender sees events + rising threat score

---

## Phase 5 — Threat scoring + auto-lock (Hours 14–18)
### Goal
System locks itself based on suspicious behavior.

### Start rule-based
Signals:
- “new IP”
- “odd hour”
- “too many attempts quickly”
- “honeypot interaction”

Rule:
- If score exceeds threshold → `locked=true`, threat_level high, log the reason

### Checkpoint
- You can trigger lock reliably by a scripted sequence

---

## Phase 6 — Optional AI “Autopsy Report” (Hours 18–21)
### Goal
Agentic explanation for judges.

- Generate a short report (5–8 sentences) when lock triggers
- Display on UI
- Add timeout + fallback message

**CrewAI is optional.** A single LLM call is acceptable and more reliable.

### Checkpoint
- Lock event produces a readable explanation consistently

---

## Phase 7 — Final polish + rehearsal (Hours 21–24)
### Goal
A stable demo that works twice in a row.

- Add “Reset demo” button (clears logs, unlocks, sets threat to 0)
- Improve Tailwind styling (overlay + dashboard)
- Rehearse on the final network setup
- Prepare a 90–120s demo script

### Final demo script
1) Show `/` (still online)
2) Show `/admin` normal
3) Trigger suspicious action → lock overlay appears
4) OLED shows LOCKED + threat
5) Press physical button → unlock
6) Optional: show honeypot + logs + AI report

---

## Risk management (what to cut if time runs out)
Cut in this order:
1) Email sending
2) CrewAI multi-agent orchestration (keep one LLM call or rule-based)
3) Fancy honeypot depth (keep 1–2 decoy pages)
Keep:
- lock/unlock loop
- OLED + button
- overlay + logs
