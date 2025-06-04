#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Cleanup function ---
# This function will be called on script exit or on receiving SIGINT/SIGTERM.
cleanup() {
  echo "\nPerforming cleanup..."
  # Deactivate virtual environment if active
  # 'type deactivate' checks if the 'deactivate' command is available (i.e., venv is active)
  if type deactivate > /dev/null 2>&1; then
    echo "Deactivating Python virtual environment..."
    deactivate
  fi
  echo "Application startup script finished."
}

# Trap EXIT, SIGINT, SIGTERM to run the cleanup function.
# EXIT is triggered on normal script termination or after a command fails (due to 'set -e').
# SIGINT (Ctrl+C) and SIGTERM are common signals for process termination.
trap cleanup EXIT SIGINT SIGTERM

# Get the directory where the script is located to ensure paths are relative to the script.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "RentRightNL Application Startup Script"
echo "===================================="

# --- Backend Setup ---
echo "\n[1/4] Setting up backend..."
cd "$SCRIPT_DIR/backend" # Change current directory to backend/

# Create Python virtual environment if it doesn't exist in backend/venv
if [ ! -d "venv" ]; then
  echo "Creating Python virtual environment (venv) in $PWD/venv..."
  python3 -m venv venv
  echo "Virtual environment created."
else
  echo "Python virtual environment (venv) already exists in $PWD/venv."
fi

# Activate virtual environment (backend/venv/bin/activate)
# shellcheck disable=SC1091
source venv/bin/activate
echo "Activated Python virtual environment ($PWD/venv/bin/activate)."

# Upgrade pip and install dependencies from requirements.txt located in the project root.
echo "Installing backend dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r "$SCRIPT_DIR/requirements.txt"
echo "Backend dependencies installed."

# Seed the database
echo "Seeding database..."
# Run seed_db.py as a module. This is executed in a subshell from the project root ($SCRIPT_DIR)
# to ensure Python's module resolution works correctly for 'backend.seed_db'.
# The Python interpreter from the active venv ($SCRIPT_DIR/backend/venv/bin/python) will be used.
(cd "$SCRIPT_DIR" && python -m backend.seed_db)
echo "Database seeded."

# --- Frontend Setup ---
echo "\n[2/4] Setting up frontend..."
# Change current directory to project root ($SCRIPT_DIR) for npm operations.
cd "$SCRIPT_DIR"

# If node_modules exists, remove it for a clean install. This is useful in environments
# like Docker to avoid issues with pre-existing, possibly incompatible modules.
if [ -d "node_modules" ]; then
  echo "Found existing node_modules directory. Removing for a clean install."
  rm -rf node_modules
fi

echo "Installing frontend dependencies (npm install)..."
npm install
echo "Frontend dependencies installed."

# Build the frontend application.
echo "Building frontend application (npm run build)..."
npm run build
echo "Frontend application built."

# --- Final Checks (Placeholder) ---
echo "\n[3/4] Performing final checks..."
# Add any other pre-run checks here if needed (e.g., environment variables).
echo "Checks complete."

# --- Run Application ---
echo "\n[4/4] Starting application..."
cd "$SCRIPT_DIR/backend" # Change current directory to backend/ to run Uvicorn.

# Ensure the Python virtual environment (backend/venv) is active for Uvicorn.
# The path 'venv/bin/activate' is relative to the current directory ($SCRIPT_DIR/backend).
echo "Ensuring Python virtual environment ($PWD/venv) is active for Uvicorn..."
# shellcheck disable=SC1091
source venv/bin/activate

# Start FastAPI server using Uvicorn.
# The backend/main.py serves static files from ../build (i.e., $SCRIPT_DIR/build).
# The API will be available on port 9000.
echo "Starting FastAPI server on http://0.0.0.0:9000"
echo "The application should be accessible at http://localhost:9000"
echo "Press Ctrl+C to stop the server and trigger cleanup."

# Using --reload for development. For production, consider removing --reload 
# and using a more robust process manager (e.g., Gunicorn with Uvicorn workers).
# Uvicorn is run from the 'backend' directory, so the ASGI app module is 'main:app'.
uvicorn main:app --host 0.0.0.0 --port 9000 --reload

# Script will block here until Uvicorn exits.
# Upon exit (normal or signaled), the 'trap cleanup EXIT' command will execute the cleanup function.
