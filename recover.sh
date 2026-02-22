#!/bin/bash
# ==============================================
# ONE-CLICK RECOVERY - AEGIS LABYRINTH
# Run this IMMEDIATELY after first SSH login
# ==============================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}==============================================${NC}"
echo -e "${GREEN}🚀 AEGIS LABYRINTH - ONE-CLICK RECOVERY${NC}"
echo -e "${BLUE}==============================================${NC}"
echo ""

# 1. Update system
echo -e "${YELLOW}[1/7]📦 Updating system packages...${NC}"
sudo apt update && sudo apt upgrade -y

# 2. Install essentials
echo -e "${YELLOW}[2/7]📦 Installing git, Python, Node.js...${NC}"
sudo apt install -y git python3-pip python3-venv nodejs npm

# 3. Clone your repo (using HTTPS - no SSH keys needed!)
echo -e "${YELLOW}[3/7]📥 Cloning repository...${NC}"
cd ~
if [ -d "crimson-hackathon" ]; then
    echo "Removing existing directory..."
    rm -rf crimson-hackathon
fi
git clone https://github.com/santiago-pelaez/crimson-hackathon.git
cd crimson-hackathon

# 4. Set up Python virtual environment
echo -e "${YELLOW}[4/7]🐍 Configuring Python environment...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn requests python-dotenv RPi.GPIO

# 5. Install frontend dependencies
echo -e "${YELLOW}[5/7]🎨 Building frontend...${NC}"
cd frontend
npm install
cd ..

# 6. Make scripts executable
echo -e "${YELLOW}[6/7]🔧 Making scripts executable...${NC}"
chmod +x scripts/*.py
chmod +x hardware/aegis_daemon.py

# 7. Create a demo command cheat sheet in home directory
echo -e "${YELLOW}[7/7]📝 Creating demo command sheet...${NC}"
cd ~
cat > demo_commands.txt << 'EOF'
===============================================
🚀 AEGIS LABYRINTH - DEMO COMMANDS
===============================================

📌 TERMINAL 1 - BACKEND:
cd ~/crimson-hackathon/backend && source ../venv/bin/activate && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

📌 TERMINAL 2 - FRONTEND:
cd ~/crimson-hackathon/frontend && npm run dev

📌 TERMINAL 3 - HARDWARE:
cd ~/crimson-hackathon/hardware && source ../venv/bin/activate && python aegis_daemon.py

📌 TO LOCK (Terminal 4):
curl -X POST http://localhost:8000/lock

📌 TO CHECK STATUS:
curl http://localhost:8000/status

📌 PI IP: 172.20.10.12
📌 FRONTEND URL: http://172.20.10.12:5173
📌 ADMIN URL: http://172.20.10.12:5173/admin

===============================================
EOF

echo -e "${BLUE}==============================================${NC}"
echo -e "${GREEN}✅ RECOVERY COMPLETE!${NC}"
echo -e "${BLUE}==============================================${NC}"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "1. Open VS Code and connect to the Pi"
echo "2. Open 3 terminals"
echo "3. Run the commands from ~/demo_commands.txt"
echo ""
echo -e "${YELLOW}📍 Quick access to commands:${NC}"
echo "   cat ~/demo_commands.txt"
echo ""
echo -e "${BLUE}==============================================${NC}"
