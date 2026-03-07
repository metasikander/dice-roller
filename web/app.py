#!/usr/bin/env python3
# coding: utf-8
"""Flask web interface for the dice roller."""

import os
import sys

# Ensure the repo root is on the import path so dice.py is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, render_template, request, jsonify

from dice import dice_roller, stats_roll, dir_roll

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """Serve the main page."""
    return render_template("index.html")


@app.route("/roll", methods=["POST"])
def roll() -> tuple:
    """Roll dice from a notation string and return JSON."""
    notation = request.form.get("notation", "").strip()
    if not notation:
        return jsonify({"error": "No dice notation provided."}), 400

    try:
        total, rolls = dice_roller(notation)
        breakdown = [
            {"sides": int(r.split("/")[1]), "value": int(r.split("/")[0])}
            for r in rolls
        ]
        return jsonify({"total": total, "rolls": breakdown})
    except ZeroDivisionError:
        return jsonify({"error": "You cannot divide by zero."}), 400
    except (ValueError, IndexError):
        return jsonify({"error": f"Invalid dice notation: {notation}"}), 400


@app.route("/direction", methods=["POST"])
def direction() -> tuple:
    """Return a random compass direction as JSON."""
    return jsonify({"direction": dir_roll()})


@app.route("/stats", methods=["POST"])
def stats() -> tuple:
    """Return a D&D 5e stat block roll as JSON."""
    return jsonify({"stats": stats_roll()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
