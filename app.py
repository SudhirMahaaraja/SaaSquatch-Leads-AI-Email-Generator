from flask import Flask
from controllers.page_controller import page_bp
from controllers.email_controller import email_bp

app = Flask(__name__, static_folder="static", template_folder="templates")

# Register blueprints
app.register_blueprint(page_bp)
app.register_blueprint(email_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
