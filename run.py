#!/usr/bin/env python3
"""Run the BMW 02 Tracker application."""

from app import create_app
from app.seed import seed_database

app = create_app()

with app.app_context():
    seed_database()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
