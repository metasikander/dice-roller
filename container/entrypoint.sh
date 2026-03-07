#!/bin/sh
# Entrypoint wrapper for dice-roller container.
# Routes to either CLI mode (default) or web mode.
#
# Usage:
#   docker run dice-roller 2d8+6        # CLI mode
#   docker run dice-roller web          # Web mode

if [ "$1" = "web" ]; then
    # Web mode: start Flask server (use uv virtual environment)
    exec .venv/bin/python web/app.py
else
    # CLI mode: pass all arguments to the roll script
    exec python roll "$@"
fi
