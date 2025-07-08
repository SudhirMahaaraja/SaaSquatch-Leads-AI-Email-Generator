// static/js/app.js

// Populate Tone & Focus dropdowns
const toneSelect = document.getElementById('tone');
const focusSelect = document.getElementById('focus');

['Professional', 'Friendly', 'Direct', 'Casual']
  .forEach(t => toneSelect.add(new Option(t)));
['Partnership', 'Collaboration', 'Networking', 'Sales']
  .forEach(f => focusSelect.add(new Option(f)));

let currentLeadId = null;

// Open the email generator panel for a given lead
function openPanel(id) {
  currentLeadId = id;
  document.getElementById('email-panel').style.display = 'flex';
}

// Attach openPanel to global scope so inline onclick works
window.openPanel = openPanel;

// Click handler for Generate button
document.getElementById('generate').onclick = async () => {
  const tone    = toneSelect.value;
  const focus   = focusSelect.value;
  const variant = document.getElementById('variant').value;

  // Show loader, hide previous output
  document.getElementById('loader').style.display = 'block';
  document.getElementById('output').style.display = 'none';

  try {
    const resp = await fetch('/api/email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        leadId: currentLeadId,
        tone,
        focus,
        variant
      })
    });

    // If HTTP error, parse JSON error message or fallback
    if (!resp.ok) {
      let errMsg = `Status ${resp.status}`;
      try {
        const errJson = await resp.json();
        errMsg = errJson.error || errMsg;
      } catch {}
      throw new Error(errMsg);
    }

    const data = await resp.json();
    console.log("✅ Server response:", data);

    // Display subject & body (or placeholders if empty)
    document.getElementById('subject').innerText = data.subject || "[no subject returned]";
    document.getElementById('body').innerText    = data.body    || "[no body returned]";

    document.getElementById('output').style.display = 'block';
  } catch (e) {
    console.error("❌ Error generating email:", e);
    alert("Error generating email:\n" + e.message);
  } finally {
    document.getElementById('loader').style.display = 'none';
  }
};

// Copy text helper
function copyText(id) {
  const text = document.getElementById(id).innerText;
  navigator.clipboard.writeText(text)
    .then(() => alert('Copied to clipboard!'))
    .catch(err => alert('Copy failed: ' + err));
}

// Open in default mail client
function openInEmail() {
  const subject = encodeURIComponent(document.getElementById('subject').innerText);
  const body    = encodeURIComponent(document.getElementById('body').innerText);
  window.location.href = `mailto:?subject=${subject}&body=${body}`;
}

// Expose helpers to global scope
window.copyText    = copyText;
window.openInEmail = openInEmail;
