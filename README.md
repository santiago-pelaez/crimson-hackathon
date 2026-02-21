# Aegis Labyrinth (GhostTrap Variant)
**Reinvent the firewall into a physical, agentic labyrinth.**  
Aegis Labyrinth is a hackathon prototype that combines **deception (honeypot)**, **agentic AI reasoning**, and **hardware-based physical authorization** to protect “high-risk admin actions” even if an attacker steals the password.

Instead of a firewall that is only a *wall* (allow/deny), Aegis Labyrinth becomes a **maze**:
- normal users browse normally (storefront stays up)
- suspicious users get pushed into a **decoy admin vault** (honeypot)
- sensitive admin actions trigger a **Selective Freeze**
- the freeze can only be cleared by a **physical button press on the Raspberry Pi**
- LEDs + servos make the invisible cyber state **physically visible**

---

## Table of Contents
- [What You’re Building (High-Level)](#what-youre-building-high-level)
- [Core Idea: The Mechanical Gatekeeper](#core-idea-the-mechanical-gatekeeper)
- [System Components](#system-components)
- [How “Selective Freeze” Works](#how-selective-freeze-works)
- [Honeypot / Labyrinth Design](#honeypot--labyrinth-design)
- [Agentic Crew (Practical Implementation)](#agentic-crew-practical-implementation)
- [Frontend Plan](#frontend-plan)
- [Hardware Plan](#hardware-plan)
- [Step-by-Step Build Guide (24-hour Friendly)](#step-by-step-build-guide-24-hour-friendly)
- [Demo Script (What Judges Will See)](#demo-script-what-judges-will-see)
- [Stretch Goals](#stretch-goals)
- [Safety / Ethics](#safety--ethics)

---

## What You’re Building (High-Level)
A single Raspberry Pi hosts:
1. **Storefront (public site)** — always available
2. **Admin Vault (real admin UI)** — sensitive actions can be frozen
3. **Labyrinth Admin (honeypot UI)** — a decoy admin that logs attacker behavior
4. **Defender Dashboard** — live event feed, threat score, and vault state
5. **Hardware Guardian** — LEDs + servo(s) + button for physical authorization
6. **Optional AI Reporter** — produces “what happened” summaries

---

## Core Idea: The Mechanical Gatekeeper
Traditional security is often a single wall:
- If a hacker gets your admin password, they get through.

Aegis Labyrinth adds a **Physical Deadlock**:
- Even with a stolen password, high-risk actions are blocked unless someone **physically presses a button on the Pi** (on the desk).
- That button press creates a short unlock window (e.g., 60 seconds) so the action can proceed.

This is the “reinvent the wheel” moment:
> A firewall becomes a **physical guardian** + **deception maze** + **explainable SOC assistant**.

---

## System Components
### 1) Web Backend (FastAPI or Flask)
- Serves storefront + admin pages
- Implements “Selective Freeze” policy (vault freeze/unlock)
- Emits structured security events (JSON-like objects)
- Exposes APIs for dashboard + hardware daemon

### 2) Hardware Daemon (runs on the Pi)
- Reads the **physical button**
- Controls LEDs and servo(s)
- Sends “unlock approved” events to backend

### 3) AI/Agent Module (optional)
- Reads recent events
- Labels behavior (normal vs suspicious)
- Recommends actions from a **safe menu**
- Generates an “incident autopsy” report

> Recommendation for reliability: keep enforcement deterministic; use AI for explanation + recommendations.

---

## How “Selective Freeze” Works
Selective Freeze is a *policy layer* that applies only to sensitive routes.

### Terminology
- **Vault Frozen:** sensitive actions are blocked; UI shows lock overlay
- **Vault Unlocked:** sensitive actions allowed for a short time window

### Vault state (simple state machine)
- **Normal:** vault not frozen
- **Frozen:** sensitive endpoints return `403 PhysicalAuthRequired`
- **Temporarily Unlocked:** after button press, allow actions until `unlocked_until`

### Sensitive actions to protect (pick 3–5)
Examples:
- Delete user
- Update pricing
- Export data
- Update settings
- View “financials”

---

## Honeypot / Labyrinth Design
The honeypot is **a decoy admin interface** served by the same web app.

### Labyrinth routes (example)
- `/labyrinth/admin` (fake login)
- `/labyrinth/admin/dashboard` (fake console)
- `/labyrinth/admin/export-db` (fake export)
- `/labyrinth/admin/users/delete` (fake delete)
- `/labyrinth/admin/settings` (fake settings)

Everything in the labyrinth:
- **looks real**
- **does nothing real**
- **logs everything** (paths, login attempts, button clicks)

---

## Agentic Crew (Practical Implementation)
You can present this as a crew of agents, but implement it safely:

### The Sentry (Observer)
- Watches events (logins, admin actions, honeypot interactions)
- Produces a threat score (0–100) + reasons

### The Architect (Strategist)
- Chooses response from a fixed safe menu:
  - `freeze_vault`
  - `route_to_labyrinth`
  - `rate_limit`
  - `do_nothing`

### The Warden (Hardware Liaison)
- Moves servo(s), sets LEDs
- Enforces the physical requirement:
  - vault stays frozen until **button press** is seen

### Optional: Reporter
- Generates a human-friendly “autopsy” summary:
  - what happened
  - why it was suspicious
  - what we did
  - recommendations

---

## Frontend Plan
You’ll have three frontends (all can be simple HTML/CSS for speed):

1. **Storefront**
   - basic landing page; always works

2. **Admin Vault**
   - buttons to trigger sensitive actions
   - when frozen: shows a **lock overlay**
     - “Physical authentication required on Aegis device”

3. **Defender Dashboard**
   - threat score gauge
   - vault state (Frozen / Unlocked until time)
   - event feed (last 50 events)
   - controls: reset, arm/disarm, unlock status

---

## Hardware Plan
### Minimum hardware
- Raspberry Pi
- 1 button (GPIO input)
- 1 LED (or RGB LED)
- 1 servo (optional second servo if you have time)

### Suggested mapping
- **LED**
  - green = SAFE
  - blinking red = INVESTIGATING / vault frozen
  - solid red = CRITICAL / trap active

- **Servo 1: Traffic Spinner**
  - 0° = Safe
  - 90° = Suspicious
  - 180° = Attack / Frozen

- **Servo 2 (optional): Auth Lever**
  - moves to “LOCKED” when frozen
  - moves to “UNLOCKED” when button approves

---

# Step-by-Step Build Guide (24-hour Friendly)

## Step 0 — Prep (30 minutes)
1. Put Pi + attacker laptop + defender laptop on the same network (hotspot/router).
2. Confirm:
   - you can reach the Pi IP from both laptops
3. Decide:
   - Framework (FastAPI vs Flask)
   - One servo vs two
   - AI module yes/no

**Goal:** controlled environment = reliable demo.

---

## Step 1 — Build the Web App Skeleton (1–2 hours)
Create these pages first (no security logic yet):
- `GET /` storefront
- `GET /admin` admin vault page
- `POST /admin/pricing/update` (fake action endpoint)
- `POST /admin/users/delete` (fake action endpoint)
- `GET /dashboard` defender dashboard page

**Goal:** you can click admin buttons and see requests arriving.

---

## Step 2 — Add Event Logging (1–2 hours)
Whenever someone hits:
- `/admin`
- any admin POST action
- any labyrinth route

Record an event with:
- timestamp
- IP
- route
- event_type
- optional metadata (user-agent, attempted username)

Maintain:
- in-memory list of last N events (N=200)
- per-IP counters (basic dict)

**Goal:** you can display an event list in the dashboard.

---

## Step 3 — Implement Selective Freeze (Core Feature) (2–3 hours)
1. Create global vault state:
   - `vault_frozen: bool`
   - `vault_unlocked_until: time or null`
2. Add a middleware/decorator for sensitive routes:
   - if vault frozen AND current time > unlocked_until:
     - return `403 PhysicalAuthRequired`
3. Add endpoints:
   - `POST /api/freeze` (freeze vault)
   - `POST /api/unfreeze` (manual for testing)
   - `GET /api/vault-status` (frozen? unlocked until?)

**Goal:** you can freeze vault and see admin actions blocked.

---

## Step 4 — Frontend “Lock Overlay” (1–2 hours)
In the admin vault UI:
- when a sensitive action fails with `PhysicalAuthRequired`:
  - display overlay with:
    - lock icon
    - message: “Press the Aegis device button to approve”
- optionally poll `/api/vault-status` every 1s:
  - hide overlay when unlocked

**Goal:** the freeze becomes visually obvious.

---

## Step 5 — Hardware Daemon (Button → Unlock) (2–3 hours)
Create a small Python process on the Pi that:
1. Reads the button GPIO
2. On press:
   - calls backend endpoint `POST /api/approve-unlock`
3. Controls LED + servo based on backend state:
   - poll `/api/vault-status` and `/api/threat-status`
   - set LED and servo accordingly

Backend behavior on `/api/approve-unlock`:
- sets `vault_unlocked_until = now + 60 seconds`

**Goal:** pressing the physical button actually unlocks the admin vault.

---

## Step 6 — Add the Labyrinth Honeypot (2–4 hours)
Build decoy pages:
- `/labyrinth/admin` fake login
- `/labyrinth/admin/dashboard` fake dashboard
- fake actions (export, settings, delete)

Log everything. Make it look convincing with simple CSS.

Optional routing rule:
- if an IP becomes suspicious, redirect `/admin` → `/labyrinth/admin`

**Goal:** you have a believable trap + logs to show judges.

---

## Step 7 — Add Threat Scoring + Responses (1–3 hours)
Implement a simple score per IP:
- hit admin pages rapidly → +points
- repeated failed honeypot logins → +points
- clicking “export db” → +points

Then:
- if score > threshold:
  - freeze vault
  - route them to labyrinth
  - set hardware state to “investigating/critical”

**Goal:** the system becomes “agentic”: observe → decide → act.

---

## Step 8 (Optional) — AI Autopsy Report (1–2 hours)
When a freeze happens, generate a report from a structured event summary:
- “IP X attempted these actions…”
- “Triggered freeze because…”
- “Recommendations…”

Display it on `/dashboard`.

**Goal:** judges get a clear explanation.

---

# Demo Script (What Judges Will See)
1. Start SAFE:
   - LED green, servo low
   - admin actions work normally

2. Simulate attacker:
   - attacker laptop hits `/admin` and starts “suspicious” actions
   - system threat score rises

3. Vault freezes:
   - admin UI shows lock overlay
   - LED red, servo moves to locked position

4. Physical unlock:
   - you press the Pi button
   - vault unlocks for 60 seconds
   - you perform the sensitive action successfully

5. Show labyrinth:
   - attacker is routed into fake admin console
   - dashboard shows logs of what they tried

6. Optional:
   - AI “autopsy” report shown and read aloud

---

## Stretch Goals
- Add SSH brute-force detection (only after web + hardware is solid)
- Add a second servo (“auth lever”)
- Rate limiting for suspicious IPs
- Email notification (“Mom, I blocked a suspicious change attempt…”)
- Export logs as JSON / CSV

---

## Safety / Ethics
- Run only on a local demo network.
- Do not collect real credentials.
- Make honeypot clearly a demo environment in your presentation.
- Never deploy on networks you don’t own/have permission to test.

---
