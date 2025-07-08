# SaaSquatch Leads – AI Email Generator (MVC + Groq)

A lean, 5-hour proof-of-concept web application that transforms a static lead list into personalized outreach emails—powered by Groq's free `gemma-2-9b-it` model. Built in Python with Flask following a clean MVC structure and featuring a dark-mode, CRM-inspired UI.

---

## 🚀 Key Features

- **Dark-mode CRM UI**  
  Side navigation, top bar, lead table with action icons, slide-in email panel  
- **AI-Powered Email Generation**  
  Choose tone (Professional, Friendly, Direct, Casual), focus (Partnership, Collaboration, Networking, Sales), and A/B variant  
- **Groq API Integration**  
  Direct REST call to `https://api.groq.com/openai/v1/chat/completions` with `gemma-2-9b-it` model  
- **Copy & Send**  
  "Copy Subject" / "Copy Body" buttons and "Open in Email" (mailto:) link  
- **MVC Architecture**  
  - **Models:** `models/lead_model.py` (in-memory lead dataset)  
  - **Views:** `templates/index.html` (Jinja template with inline CSS)  
  - **Controllers:**  
    - `controllers/page_controller.py` (renders the main UI)  
    - `controllers/email_controller.py` (handles AI requests)  
  - **Static:** `static/js/app.js` (client-side interactivity)  

---

## 📂 Project Structure

```text
flask_saasquatch_leads/
│
├── app.py                     # Flask app entrypoint & blueprint registration
├── requirements.txt           # Python dependencies
│
├── models/
│   └── lead_model.py          # Sample in-memory list of leads
│
├── controllers/
│   ├── page_controller.py     # Renders the home page
│   └── email_controller.py    # Handles /api/email requests
│
├── templates/
│   └── index.html             # Main UI with inline CSS
│
└── static/
    └── js/
        └── app.js             # Client-side logic for panel & API calls
```

---

## 🔧 Prerequisites

* Python 3.8+
* pip
* A free Groq API key (sign up at [https://groq.com](https://groq.com))

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/saasquatch-leads-mvc-groq.git
   cd saasquatch-leads-mvc-groq
   ```

2. **Create & activate a virtual environment**

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your Groq API key**
   In `controllers/email_controller.py`, replace the placeholder:

   ```python
   GROQ_KEY = "YOUR_REAL_GROQ_API_KEY_HERE"
   ```

   with your actual key.

---

## ▶️ Running the App

```bash
python app.py
```

* The Flask development server will start on `http://127.0.0.1:5000/`.
* Open that URL in your browser.
* Click the ✉️ icon next to any lead to open the email panel.
* Select your tone, focus, and variant. Click **Generate**.
* Copy or "Open in Email" to send.

---

## 🛠️ MVC Breakdown

### Models (`models/lead_model.py`)

Holds a simple list of leads (company, industry, employees, revenue, location). Easily replaceable with a real database or API.

### Views (`templates/index.html`)

A single Jinja template containing:

* Inline CSS for a self-contained dark-mode layout
* Table of leads, slide-in panel markup for email generation
* Includes `<script src="{{ url_for('static', filename='js/app.js') }}">`

### Controllers

* **`page_controller.py`**
  Renders `index.html` and passes `leads` into the template context.
* **`email_controller.py`**
  Receives POSTs at `/api/email`, builds a prompt, calls Groq's REST API, parses `Subject` and `Body`, and returns JSON.

### Static JS (`static/js/app.js`)

Handles:

* Opening the slide-in panel
* Populating dropdowns
* `fetch()` call to `/api/email`
* Rendering subject/body or errors
* Copy to clipboard & mailto flow

---

## 📈 Extensibility & Next Steps

* **Persist leads** in a database (SQLite, PostgreSQL) instead of in-memory.
* **Add analytics** hooks to track which variant performs best.
* **Integrate CRM** (e.g., HubSpot, Salesforce) via their REST APIs.
* **Enhance UI** with filters, search, pagination.
* **Implement A/B tracking** backend to record impressions & clicks.
* **Secure API key** with a proper secrets store or environment variables.

---

## 📝 License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙌 Acknowledgments

* Built in 5 hours as a **Quality-First** POC for lead-generation workflows.
* Powered by [Groq](https://groq.com) `gemma-2-9b-it` model.
* Sudhir