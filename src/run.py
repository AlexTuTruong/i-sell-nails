"""Runfile, run with 'python3 run.py'"""
import uvicorn
from main import app


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
