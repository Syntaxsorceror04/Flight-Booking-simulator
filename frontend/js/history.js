// js/history.js
import { getHistory } from './api.js';

const form = document.getElementById('historyForm');
const emailInput = document.getElementById('historyEmail');
const historyList = document.getElementById('historyList');
const historyMessage = document.getElementById('historyMessage');

function showMessage(text, type='error') {
  historyMessage.innerHTML = text ? `<div class="${type === 'error' ? 'error' : 'success'}">${text}</div>` : '';
}

function createHistoryItem(b) {
  // b is expected to be a booking object from backend. We must not invent fields.
  const item = document.createElement('div');
  item.className = 'card history-item';

  const left = document.createElement('div');
  left.style.minWidth = '0';
  left.innerHTML = `
    <div style="font-weight:700;">${b.flight?.airline_name || b.flight_number || b.flight || 'Booking'}</div>
    <div class="small-muted">${b.flight?.origin || b.origin || ''} → ${b.flight?.destination || b.destination || ''}</div>
    <div class="small-muted">${b.pnr ? 'PNR: ' + b.pnr : ''}</div>
  `;

  const right = document.createElement('div');
  right.style.textAlign = 'right';
  right.innerHTML = `
    <div class="small-muted">Status</div>
    <div style="font-weight:700;">${b.status || 'N/A'}</div>
    <div style="margin-top:8px;">
      <a class="btn" href="receipt.html?pnr=${encodeURIComponent(b.pnr || '')}" style="text-decoration:none; padding:6px 8px;">View</a>
    </div>
  `;

  item.appendChild(left);
  item.appendChild(right);
  return item;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  historyList.innerHTML = '';
  showMessage('', '');
  const email = emailInput.value.trim();
  if (!email || !/^\S+@\S+\.\S+$/.test(email)) {
    showMessage('Please enter a valid email address.', 'error');
    return;
  }
  try {
    const data = await getHistory(email);
    if (!Array.isArray(data) || data.length === 0) {
      showMessage('No bookings found for this email.', 'error');
      return;
    }
    data.forEach(b => {
      const node = createHistoryItem(b);
      historyList.appendChild(node);
    });
    showMessage(`Found ${data.length} booking(s).`, 'success');
  } catch (err) {
    console.error(err);
    const text = err && err.body && err.body.message ? err.body.message : (err.body || err.message || 'Failed to fetch history.');
    showMessage(`Error: ${text}`, 'error');
  }
});