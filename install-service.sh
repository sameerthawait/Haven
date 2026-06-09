#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_FILE="$SCRIPT_DIR/haven-ui.service"

if [ ! -f "$SERVICE_FILE" ]; then
  echo "Error: haven-ui.service not found in $SCRIPT_DIR"
  exit 1
fi

echo "Installing Haven UI service..."
echo "Make sure you've edited haven-ui.service with your username and paths first!"
echo ""

sudo cp "$SERVICE_FILE" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable haven-ui
sudo systemctl start haven-ui
sudo systemctl status haven-ui
