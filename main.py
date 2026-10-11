"""
Entry point for running the Cold Storage system from the project root.
You can run this using: py -3 main.py
Or run directly inside backend/: py -3 backend/app.py
"""
import sys
import os

# Add backend directory to module search path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app import app, db

if __name__ == "__main__":
    db.init_db()
    print("=" * 60)
    print(" Cold Storage Backend Running at: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=True)
