# Aegis Lock
**A Full-Stack Approach to a Penetration Test**

Aegis Lock is a physical security feature to deter attackers, distinguish them from authorized users, and physically approve authorized users, should it be escalted to that level. It's a twist on a physical passkey entirely programmed into a deadlock that can’t be bypassed remotely.

This repository contains a full-stack web application built for penetration testing exercises and to demonstrate a working simulated full-stack website. It includes both frontend and backend components running in **Docker containers**. The goal is to simulate brute force cyber threats and use an LLM to recognize "automation" or unusual login attempts such as VPN detection and IP geolocation.

The environment allows security professionals and penetration testers to **simulate** a brute force attack and malicious login attempts, while training an API to monitor and react to suspicious activities.

### Key Components
- **Frontend**: The web interface simulates a bakery and a log on portal using React.js.
- **Backend**: The backend is in python built using FastAPI, which utilizes LLM Gemini 2.5 Flash to assess suspicious activity.
- **Database**: A test database to contain user data for testing. (For the home stretch)
- **Docker**: a fully containerized environment using Docker for easy setup and testing.
- **Physical Authorization**: A physical button programmed on a Raspberry Pi to act as a physical passkey to bypass "threat" assements from login attempts by an actual authorized user.

---

### Threat Model and Test Scenarios

This application implements a **dynamic threat model** based on user behavior, such as login attempts, IP geolocation, VPN usage, and other factors. The goal is to **detect and react to potential security threats** like brute-forcing, account sharing, and unauthorized access from suspicious geolocations.

#### **Threat Levels**:
1. **Green (Low Threat <= 30)**: 
   - Users located in **West Coast** regions (Seattle, Portland, California) which simulate where our small company is based, are assumed to be green.
   - 5 failed login attempt adds 15 points to our threat model, and a 30-second timeout occurs after every 5th failed attempt.
   
2. **Yellow (Medium Threat < 60)**:
   - Users accessing via **domestic VPNs** or showing suspicious behavior patterns.
   - **20 failed login attempts** or reaching 60 points automatically escalates to a **Red** threat.
   
3. **Red (High Threat >= 60)**:
   - **Non-U.S. IP addresses** or users showing **brute-force attack patterns**.
   - After the threshold has been reached, every **3 failed login attempts** a 3-minute timeout is applied, and the user is flagged as high-risk.

### Attack Scenarios for the Penetration Test
- **Brute Force Attacks** (IP rotation, multiple attempts from the same user)
- **VPN and Geolocation Spoofing** (Test for IP geolocation filters and VPN detection)
- **Credential Stuffing** (Test for protection against automated login attempts)

#### Manual Approval and Backend Terminal Function

## **1. Manual Approval Process Overview**

When suspicious activity is detected, such as multiple failed login attempts, VPN usage, or accessing from a suspicious IP, users are evaluated and properly escalated to the **manual review queue**. This ensures legitimate users aren't incorrectly flagged as attackers and that potential threats are carefully examined before any action is taken. For most attacks, it is escalated to a threshold of 60. Human error can reasonably be categorized in the medium threshold.

The **manual approval** process is facilitated through a backend terminal, which provides a real-time review of suspicious behavior. The terminal enables security personnel to observe **metadata** about each user’s activity to take appropriate action (e.g., approve access or lockout).

## **2. Priority System and Queues**

The approval system operates on a two-tiered queue system for manual review, with a priority hierarchy to focus aid on human errors typically evaluated at a threat level medium.

## **3. Backend Terminal Functionality**

The **backend terminal** is used for monitoring suspicious activities. System administrators can review login attempts to physically approve logins.

#### **3.1. Real-Time Review Dashboard**
- **Pending Reviews**: The backend terminal displays users who have been escalated to the Yellow or Red queues. Each entry provides metadata and the context needed for making decisions.
  
- **Metadata Collected**: For each user under review, the following information is displayed:
  - **IP Address**: The geolocation of the user’s IP, indicating if the user is in a trusted region (e.g., West Coast U.S.) or flagged as suspicious (e.g., outside the U.S.).
  - **Failed Login Attempts**: A record of all failed login attempts with **time stamps** and **IP addresses**.
  - **Geolocation Data**: Geographic details of the IP address, including country and city, to help determine whether the access is likely legitimate or suspicious.
  - **VPN Detection**: The system checks whether the user is accessing from a **VPN** or **proxy**, and flags them if VPN usage is detected.

#### **3.2. Decisions from Backend Review**
Once the metadata has been reviewed, the sys-admin can take action in a few ways:
  - **Approve Access**: If no malicious intent is detected, the user can be allowed to proceed with their access.
  - **Lock Account**: If there is suspicion but no clear malicious intent, the user's account can be temporarily locked for further review or investigation, or, if contacted by the user and verified, to be physically bypassed by pressing the Raspberry Pi passkey.

## Setting Up the Lab

### Prerequisites

Ensure that the following software is installed on your local machine:
- [Docker](https://www.docker.com/products/docker-desktop)
- A terminal or command-line interface (CLI) tool

---
### Clone the Repository

```bash
git clone https://github.com/yourusername/full-stack-penetration-testing-lab.git
cd full-stack-penetration-testing-lab
```
