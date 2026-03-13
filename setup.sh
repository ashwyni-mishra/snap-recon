#!/bin/bash

# Snap-Recon Setup Script for Linux/Kali
# Handles home directory automation and sudo for system tasks.

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Determine actual user and home directory
ACTUAL_USER=$(logname || echo $USER)
USER_HOME=$(eval echo ~$ACTUAL_USER)
TARGET_DIR="$USER_HOME/snap-recon"

echo -e "${BLUE}[*] Initializing Snap-Recon Environment...${NC}"

# Ensure sudo is available
if ! command -v sudo &> /dev/null; then
    echo -e "${RED}[!] sudo command not found. Please install it or run as root.${NC}"
    exit 1
fi

# 1. Install system dependencies
echo -e "${BLUE}[*] Checking for system dependencies (requires sudo)...${NC}"
sudo apt update && sudo apt install -y python3-venv python3-pip git

# 2. Check current location vs desired home location
CURRENT_DIR=$(pwd)

if [ "$CURRENT_DIR" != "$TARGET_DIR" ]; then
    echo -e "${BLUE}[*] Setting up framework in $TARGET_DIR...${NC}"
    if [ ! -d "$TARGET_DIR" ]; then
        sudo mkdir -p "$TARGET_DIR"
        sudo cp -r . "$TARGET_DIR"
        sudo chown -R $ACTUAL_USER:$ACTUAL_USER "$TARGET_DIR"
    fi
    cd "$TARGET_DIR" || exit 1
fi

# 3. Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${BLUE}[*] Creating virtual environment...${NC}"
    python3 -m venv venv
    sudo chown -R $ACTUAL_USER:$ACTUAL_USER venv
fi

# 4. Install framework
echo -e "${BLUE}[*] Installing dependencies and framework...${NC}"
# Use the full path to venv pip to ensure it's installed correctly
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt
./venv/bin/pip install .

# 5. Add alias to .bashrc
BASHRC="$USER_HOME/.bashrc"
ALIAS_LINE="alias snaprecon='$TARGET_DIR/venv/bin/snaprecon'"

if ! grep -q "alias snaprecon=" "$BASHRC"; then
    echo -e "${BLUE}[*] Adding snaprecon alias to $BASHRC...${NC}"
    echo "$ALIAS_LINE" >> "$BASHRC"
    echo -e "${GREEN}[✓] Alias added!${NC}"
else
    # Update existing alias
    sed -i "s|alias snaprecon=.*|$ALIAS_LINE|" "$BASHRC"
    echo -e "${BLUE}[*] Updated existing alias in $BASHRC.${NC}"
fi

echo -e "${GREEN}[✓] Setup complete!${NC}"
echo -e "${BLUE}[*] Please restart your terminal or run: ${NC}source ~/.bashrc"
echo -e "${BLUE}[*] Then run: ${NC}snaprecon --help"
