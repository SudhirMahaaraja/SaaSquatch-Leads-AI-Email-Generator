from flask import Blueprint, render_template
from models.lead_model import leads

page_bp = Blueprint("page", __name__)

@page_bp.route("/")
def home():
    # Renders the main table + email panel template
    return render_template("index.html", leads=leads)
