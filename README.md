# Aegis Lock
**A Full-Stack Approach to a Penetration Test**

Aegis Lock is a physical security feature to deter attackers, distinguish them from authroized users, and physially approve authorized users. A sort of twist to a physical passkey entirely programed in to a deadlock that can’t be bypassed remotely.

This repository contains a full-stack web application built for penetration testing exercises and to demonstrate a working simulated full-stack website.
It includes both frontend and backend components running in **Docker containers**. The goal is to simulate brute force cyber threats and use an LLM to recognize "automation" or unusual login attempts such as VPN detection and IP geolocation.

The environment allows security professionals and penetration testers to **simulate** a brute force attack and malicious login attempts, while training an API to monitor and react to suspicious activities.

### Key Components
- **Frontend**: Web interface simulating a bakery and an admin portal using react.js.
- **Backend**: Python built using Fast API which utilizes LLM Gemini 2.5 Flash to assess activity.
- **Database**: some db, containing user data for testing.     // For home stretch
- **Docker**: Fully containerized enviornment using Docker for easy setup and testing.
- **Physical authorization**: A physical button programmed on a Rasberry Pi to act as a physical passkey to bypass "high threat" assessed login attempts from an authorized user. 
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
- The Raspberry Pi device’s **LCD shows `LOCKED` + `Threat: XX/100`**
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
- **Grove LCD RGB Backlight v4.0** (I2C) + cable/adapter to connect to Pi I2C
- **Momentary push button** (tactile) (or Grove button module)
- **Jumper wires** / Grove-to-Dupont adapter (depending on whether you have a Grove Base HAT)
- (Bring-up recommended) HDMI/keyboard for debugging (headless is possible)

> If you have a Grove Base HAT for Raspberry Pi, wiring is plug-and-play (recommended).
> Without a HAT, you’ll need a Grove-to-Dupont cable or an equivalent adapter.

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
- updates the Grove LCD text + RGB backlight
  - SAFE → green
  - WARNING → yellow/blue (team choice)
  - LOCKED → red + “Press button”
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
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is currently not compatible with SWC. See [this issue](https://github.com/vitejs/vite-plugin-react/issues/428) for tracking the progress.

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
