#!/bin/bash
# run.sh
echo "Starting LLM Knowledge Extractor..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required"
    exit 1
fi

# Create venv if doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and install
source venv/bin/activate
pip install -q -r requirements.txt

# Check .env
if [ ! -f ".env" ]; then
    echo "Creating .env from example..."
    cp .env.example .env 2>/dev/null || echo "OPENAI_API_KEY=mock" > .env
fi

# Start server
echo "Starting server on http://localhost:8000"
echo "API docs at http://localhost:8000/docs"
uvicorn app.main:app --reload