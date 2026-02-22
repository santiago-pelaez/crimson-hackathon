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

### Threat Model and Test Scenarios

This application implements a **dynamic threat model** based on user behavior, such as login attempts, IP geolocation, VPN usage, and other factors. The goal is to **detect and react to potential security threats** like brute-forcing, account sharing, and unauthorized access from suspicious geolocations.

#### **Threat Levels**:
1. **Green (Low Threat <= 30)**: 
   - Users located in **West Coast** regions (Seattle, Portland, California) which simulates where our small company is based in are assumed to be green.
   - Each failed login attempt adds 15 points to our threat model and a 30 second timeout after every 5 failed attempts.
   
2. **Yellow (Medium Threat < 60)**:
   - Users accessing via **domestic VPNs** or from suspicious behavior patterns.
   - **20 failed login attempts** or reaching 60 points automatically escalates to a **Red** threat.
   
3. **Red (High Threat >= 60)**:
   - **Non-U.S. IP addresses** or users showing **brute-force attack patterns**.
   - After **3 failed login attempts**, a 3-minute timeout is applied, and the user is flagged as high-risk.

### Attack Scenarios for the Penetration Test
- **Brute Force Attacks** (IP rotation, multiple attempts from the same user)
- **VPN and Geolocation Spoofing** (Test for IP geolocation filters and VPN detection)
- **Credential Stuffing** (Test for protection against automated login attempts)

## Manual Approval and Backend Terminal function

## **1. Manual Approval Process Overview**

When suspicious activity is detected such as multiple failed login attempts, VPN usage, or accessing from a suspicious IP, users are evaluated and properly escalated to the **manual review queue**. This ensures legitimate users aren't incorrectly flagged as attackers and that potential threats are carefully examined before any action is taken. For most attacks, it is escallated to a threshold of 60. Human error can reasonably be categorized in the medium threshold.

The **manual approval** process is facilitated through a backend terminal, which provides a real-time review of suspicious behavior. The terminal enables security personnel to observe **metadata** about each user’s activity to take appropriate action (e.g., approve access or lockout).

## **2. Priority System and Queues**

The approval system operates on a two-tiered queue system for manual review, with a priority hierarchy to focus aid on human-errors typically evaluated at a threat level medium.

## **3. Backend Terminal Functionality**

The **backend terminal** is used for monitoring suspicious activities. System administrators can review login attempts to physically approve logins.

#### **3.1. Real-Time Review Dashboard**
- **Pending Reviews**: The backend terminal displays users who have been escalated to  Yellow or Red queues. Each entry provides metadata and the context needed for making decisions.
  
- **Metadata Collected**: For each user under review, the following information is displayed:
  - **IP Address**: The geolocation of the user’s IP, indicating if the user is in a trusted region (e.g., West Coast U.S.) or flagged as suspicious (e.g., outside the U.S.).
  - **Failed Login Attempts**: A record of all failed login attempts with **time stamps** and **IP addresses**.
  - **Geolocation Data**: Geographic details of the IP address, including country and city, to help determine whether the access is likely legitimate or suspicious.
  - **VPN Detection**: The system checks whether the user is accessing from a **VPN** or **proxy**, and flags them if VPN usage is detected.

#### **3.2. Decisions from Backend Review**
Once the metadata has been reviewed, the sys-admin can take action in a few ways:
  - **Approve Access**: If no malicious intent is detected, the user can be allowed to proceed with their access.
  - **Lock Account**: If there is suspicion but no clear malicious intent, the user's account can be temporarily locked for further review or investigation or, in contacted by the user and verified, to be physically bypassed by pressing Rasberry Pi passkey.

## Setting Up the Lab

### Prerequisites

Ensure that the following software is installed on your local machine:
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)
- A terminal or command-line interface (CLI) tool
---

### Clone the Repository

```bash
git clone https://github.com/yourusername/full-stack-penetration-testing-lab.git
cd full-stack-penetration-testing-lab
```






// Edit this
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
