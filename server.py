"""
Stark Industries Hackathon — Registration Backend
===================================================
A lightweight Flask server that:
  • Serves the static frontend (index.html, squad.html, assets)
  • POST /api/register  → persists a registration to registrations.json
  • GET  /api/registrations → returns every stored registration
"""

import json
import os
import re
import threading
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
DATA_DIR = Path(__file__).resolve().parent
DATA_FILE = DATA_DIR / "registrations.json"
_registrations_lock = threading.Lock()
_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

app = Flask(__name__, static_folder=str(DATA_DIR), static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024
CORS(app)  # allow the frontend (which may be opened via file://) to reach us


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _load_registrations() -> list[dict]:
    """Read the JSON file, returning an empty list if it doesn't exist yet."""
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        return []
    return data


def _save_registrations(registrations: list[dict]) -> None:
    """Atomically write the registrations list to disk."""
    tmp_path = DATA_FILE.with_suffix(".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as fh:
            json.dump(registrations, fh, indent=2, ensure_ascii=False)
            fh.flush()
            os.fsync(fh.fileno())
        tmp_path.replace(DATA_FILE)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------
@app.route("/api/register", methods=["POST"])
def register():
    """Accept a finalized squad registration and persist it."""
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "Invalid or missing JSON body."}), 400

    # --- Validate required top-level fields ---
    team_name = payload.get("teamName")
    commander = payload.get("commander")
    members = payload.get("members")
    registration_id = payload.get("registrationId")

    errors = []
    if not isinstance(team_name, str) or not team_name.strip():
        errors.append("teamName is required.")
    if not isinstance(registration_id, str):
        registration_id = ""
    if not isinstance(commander, dict):
        errors.append("commander must be an object.")
    elif (
        not isinstance(commander.get("name"), str)
        or not commander["name"].strip()
        or not isinstance(commander.get("email"), str)
        or not commander["email"].strip()
        or not _EMAIL_PATTERN.fullmatch(commander["email"].strip())
    ):
        errors.append("commander.name and commander.email are required.")
    if not isinstance(members, list) or not members:
        errors.append("members array must contain at least one entry.")
    else:
        for index, member in enumerate(members, start=1):
            if not isinstance(member, dict):
                errors.append(f"members[{index - 1}] must be an object.")
                continue
            if not isinstance(member.get("name"), str) or not member["name"].strip():
                errors.append(f"members[{index - 1}].name is required.")
            if (
                not isinstance(member.get("email"), str)
                or not member["email"].strip()
                or not _EMAIL_PATTERN.fullmatch(member["email"].strip())
            ):
                errors.append(f"members[{index - 1}].email must be valid.")
            if not isinstance(member.get("role"), str) or not member["role"].strip():
                errors.append(f"members[{index - 1}].role is required.")

    if errors:
        return jsonify({"error": "Validation failed.", "details": errors}), 422

    # --- Build the record to store ---
    record = {
        "registrationId": registration_id or None,
        "receivedAt": datetime.now(timezone.utc).isoformat(),
        "teamName": team_name.strip(),
        "commander": {
            "name": commander["name"].strip(),
            "email": commander["email"].strip(),
        },
        "members": [
            {
                "name": (m.get("name") or "").strip(),
                "email": (m.get("email") or "").strip(),
                "role": (m.get("role") or "").strip(),
                "roleName": (m.get("roleName") or "").strip(),
            }
            for m in members
        ],
    }

    # --- Persist ---
    with _registrations_lock:
        registrations = _load_registrations()
        registrations.append(record)
        _save_registrations(registrations)

    return jsonify({"status": "ok", "registration": record}), 201


@app.route("/api/registrations", methods=["GET"])
def get_registrations():
    """Return every stored registration."""
    return jsonify(_load_registrations()), 200


# ---------------------------------------------------------------------------
# Serve static frontend files
# ---------------------------------------------------------------------------
@app.route("/")
def serve_index():
    return send_from_directory(str(DATA_DIR), "index.html")


@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(str(DATA_DIR), filename)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"[*] Registrations file: {DATA_FILE}")
    print(f"[*] Starting server at http://localhost:5000")
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "").lower() == "true",
    )
