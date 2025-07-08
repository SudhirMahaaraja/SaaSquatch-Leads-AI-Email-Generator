# controllers/email_controller.py

import os
from flask import Blueprint, request, jsonify
import requests
from models.lead_model import leads

email_bp = Blueprint("email_api", __name__)

# Hard‑code your Groq key here
GROQ_KEY = "YOUR_REAL_GROQ_API_KEY_HERE"
GROQ_URL = "Your_URL"

@email_bp.route("/email", methods=["POST"])
def generate_email():
    data = request.get_json() or {}
    lead_id = data.get("leadId")
    tone     = data.get("tone", "Professional")
    focus    = data.get("focus", "Partnership")
    variant  = data.get("variant", "A")

    lead = next((l for l in leads if l["id"] == lead_id), None)
    if not lead:
        return jsonify({"error": "Lead not found"}), 404

    prompt = (
        f"Write a {tone.lower()} outreach email for {lead['company']} "
        f"({lead['industry']}) focused on {focus.lower()}.\n"
        f"Variant: {variant}\n"
        "Include Subject: and Body:\n"
    )

    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "gemma-2-9b-it",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_completion_tokens": 1024,
        "top_p": 1
    }

    try:
        resp = requests.post(GROQ_URL, json=body, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print("❌ Groq HTTP error:", e, getattr(resp, "text", ""))
        return jsonify({"error": f"Groq API error: {e}"}), 502

    payload = resp.json()
    print("ℹ️ Groq response:", payload)

    # Validate payload shape
    choices = payload.get("choices")
    if not choices or not choices[0].get("message", {}).get("content"):
        return jsonify({"error": "Invalid response from Groq"}), 500

    content = choices[0]["message"]["content"]
    lines = [l for l in content.split("\n") if l.strip()]
    if not lines:
        return jsonify({"error": "Empty response content"}), 500

    subject = lines[0].replace("Subject:", "").strip()
    body_txt = "\n".join(lines[1:]).replace("Body:", "").strip()

    return jsonify({"subject": subject, "body": body_txt})
