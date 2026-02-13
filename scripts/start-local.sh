#!/usr/bin/env bash
# Start manim-nodes backend and frontend locally in the background.
#
# Usage:
#   ./scripts/start-local.sh          Start servers
#   ./scripts/start-local.sh stop     Stop servers
#   ./scripts/start-local.sh logs     Tail logs
#
# Logs: logs/backend.log, logs/frontend.log

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_DIR/logs"
PID_FILE="$LOG_DIR/.pids"
VENV="$HOME/.venvs/pg"

stop_servers() {
    if [ -f "$PID_FILE" ]; then
        while read -r pid; do
            kill "$pid" 2>/dev/null
        done < "$PID_FILE"
        rm -f "$PID_FILE"
        echo "Servers stopped."
    else
        echo "No servers running."
    fi
}

tail_logs() {
    tail -f "$LOG_DIR/backend.log" "$LOG_DIR/frontend.log"
}

case "${1:-start}" in
    stop)
        stop_servers
        exit 0
        ;;
    logs)
        tail_logs
        exit 0
        ;;
    start)
        ;;
    *)
        echo "Usage: $0 [start|stop|logs]"
        exit 1
        ;;
esac

# Stop any existing servers first
stop_servers 2>/dev/null

mkdir -p "$LOG_DIR"

# Check venv exists
if [ ! -f "$VENV/bin/activate" ]; then
    echo "Virtual environment not found at $VENV"
    echo "Create it with: python3 -m venv $VENV && source $VENV/bin/activate && pip install -r backend/requirements.txt"
    exit 1
fi

# Start backend
(
    source "$VENV/bin/activate"
    cd "$PROJECT_DIR"
    exec uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
) > "$LOG_DIR/backend.log" 2>&1 &
echo $! >> "$PID_FILE"

# Start frontend
(
    cd "$PROJECT_DIR/frontend"
    exec npm run dev
) > "$LOG_DIR/frontend.log" 2>&1 &
echo $! >> "$PID_FILE"

# Wait for frontend to be ready, then open browser
sleep 3
open http://localhost:5173

echo "Servers started in background."
echo "  Backend:  http://localhost:8000  → logs/backend.log"
echo "  Frontend: http://localhost:5173  → logs/frontend.log"
echo ""
echo "  Tail logs:  ./scripts/start-local.sh logs"
echo "  Stop:       ./scripts/start-local.sh stop"
