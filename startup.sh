#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "RentRightNL Application Startup Script"
echo "===================================="

# --- Backend Setup ---
echo "
[1/4] Setting up backend..."
cd "$SCRIPT_DIR/backend"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv venv
  echo "Virtual environment created."
else
  echo "Python virtual environment already exists."
fi

# Activate virtual environment
# shellcheck disable=SC1091
source venv/bin/activate
echo "Activated Python virtual environment."

# Upgrade pip and install dependencies
echo "Installing backend dependencies from requirements.txt..."
pip install --upgrade pip
# requirements.txt is in the project root ($SCRIPT_DIR)
pip install -r "$SCRIPT_DIR/requirements.txt"
echo "Backend dependencies installed."

# Seed the database
echo "Seeding database..."
# Run seed_db.py as a module from the project root directory ($SCRIPT_DIR)
# The (cd ... && ...) runs the command in a subshell, so the CWD of this script doesn't change here.
(cd "$SCRIPT_DIR" && python -m backend.seed_db)
echo "Database seeded."

cd "$SCRIPT_DIR" # Back to project root

# --- Frontend Setup ---
echo "
[2/4] Setting up frontend..."
# Ensure we are in the project root where package.json is located.
cd "$SCRIPT_DIR"

# If node_modules exists, it might be from a volume mount or a previous Docker layer
# and could have issues (e.g., platform incompatibility, corruption, incorrect permissions).
# Forcing a clean install within the container is often safer to resolve such issues.
if [ -d "node_modules" ]; then
  echo "Found existing node_modules directory. Removing for a clean install."
  rm -rf node_modules
fi

echo "Installing frontend dependencies (npm install)..."
npm install
echo "Frontend dependencies installed."

# Build the frontend
echo "Building frontend application (npm run build)..."
npm run build
echo "Frontend application built."

# --- Final Checks (Placeholder) ---
echo "
[3/4] Performing final checks..."
# Add any other checks here if needed, e.g., for required env vars if any.
echo "Checks complete."

# --- Run Application ---
echo "
[4/4] Starting application..."
cd "$SCRIPT_DIR/backend"

# Activate venv again before running uvicorn (though it should still be active in this shell)
# This is a good practice if any prior steps might have deactivated it or run in a different subshell context.
# shellcheck disable=SC1091
source venv/bin/activate

# Start FastAPI server
# The backend/main.py is configured to serve static files 
# from ../build (relative to backend/main.py, i.e., $SCRIPT_DIR/build) and its API on port 9000.
echo "Starting FastAPI server on http://0.0.0.0:9000"
echo "The application should be accessible at http://localhost:9000"

# Using --reload for development. For production, consider removing --reload and using a process manager.
uvicorn main:app --host 0.0.0.0 --port 9000 --reload

# Deactivate virtual environment on exit (though script might be terminated before this)
# This command might not be reached if uvicorn is terminated with Ctrl+C.
# Consider trap for cleanup if robust deactivation is critical.
if type deactivate > /dev/null 2>&1; then
  deactivate
fi
echo "Application stopped."
