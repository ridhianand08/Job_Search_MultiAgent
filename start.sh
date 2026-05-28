#!/bin/bash

# Start FastAPI in the background
uv run uvicorn server:app --host 0.0.0.0 --port 8000 &

# Wait for FastAPI to be ready
sleep 5

# Start Streamlit in the foreground (HF Spaces expects port 7860)
uv run streamlit run app.py --server.port 7860 --server.address 0.0.0.0