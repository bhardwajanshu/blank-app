#!/bin/bash

# AI Saree Draping Application Launcher
echo "🥻 Starting AI Saree Draping Assistant..."

# Activate virtual environment
source saree_env/bin/activate

# Check if streamlit is installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "Installing required packages..."
    pip install -r requirements.txt
fi

# Run the Streamlit app
echo "🚀 Launching application at http://localhost:8501"
streamlit run streamlit_app.py --server.port 8501 --server.headless true

echo "Application stopped."