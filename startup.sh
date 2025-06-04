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
cd "$SCRIPT_DIR/frontend"

if [ -d "node_modules" ]; then
  echo "Frontend dependencies (node_modules) already exist. Skipping npm install."
else
  echo "Installing frontend dependencies (npm install)..."
  npm install
  echo "Frontend dependencies installed."
fi

# Build the frontend
echo "Building frontend application (npm run build)..."
npm run build
echo "Frontend application built."
cd "$SCRIPT_DIR" # Back to project root

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
# shellcheck disable=SC1091
source venv/bin/activate

# Start FastAPI server
# The backend/main.py is expected to be configured to serve static files 
# from ../frontend/build and its API on port 9000.
echo "Starting FastAPI server on http://0.0.0.0:9000"
echo "The application should be accessible at http://localhost:9000"

uvicorn main:app --host 0.0.0.0 --port 9000 --reload

# Deactivate virtual environment on exit (though script might be terminated before this)
deactivate
echo "Application stopped."
