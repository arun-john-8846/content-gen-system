#!/usr/bin/env bash
# Start the ADAP Content Gen Web app locally.
cd "$(dirname "$0")"
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
fi
PORT=${PORT:-5001}
echo "Starting ADAP Content Gen Web on http://localhost:$PORT"
python3 app.py
