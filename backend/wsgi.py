"""Production WSGI entry point for gunicorn.

Run with:
    gunicorn wsgi:app

Loads environment variables from .env if present.
"""

import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app

app = create_app(os.getenv("FLASK_ENV", "production"))
