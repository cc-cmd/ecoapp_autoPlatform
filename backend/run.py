"""Development entry point for the automation platform backend.

Run with:
    python run.py

The Flask development server will start on http://127.0.0.1:5001.
"""

import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app

if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", "5001"))
    debug = os.getenv("FLASK_ENV", "development") == "development"

    # Flask's reloader (debug mode) spawns a child process with
    # WERKZEUG_RUN_MAIN=true.  Only create the real app in the child
    # to avoid generating a useless log file in the parent process.
    if not debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        app = create_app(os.getenv("FLASK_ENV", "development"))
    else:
        from flask import Flask
        app = Flask(__name__)

    app.run(host=host, port=port, debug=debug)
