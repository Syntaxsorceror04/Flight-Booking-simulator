// js/receipt.js
import { getReceipt } from './api.js';

const params = new URLSearchParams(window.location.search);
const pnr = params.get('pnr');

const receiptContainer = document.getElementById('receiptContainer');
const downloadBtn = document.getElementById('downloadBtn');

function renderReceipt(data) {
  // Expect data fields per backend contract (we must not invent fields)
  // We'll display whatever is returned in a readable way.
  const pnrVal = data.pnr || pnr || 'N/A';
  const status = data.status || 'N/A';
  const passenger = data.passenger || {};
  const flight = data.flight || {};
  const seats = data.seats || data.seats_booked || 'N/A';
  const price = data.price || data.total_price || 'N/A';

  const html = document.createElement('div');
  html.className = 'receipt-grid card';

  const left = document.createElement('div');
  left.innerHTML = `
    <div class="small-muted">PNR</div>
    <div style="font-weight:700; margin-bottom:8px;">${pnrVal}</div>

    <div class="small-muted">Status</div>
    <div style="margin-bottom:8px;">${status}</div>

    <div class="small-muted">Passenger</div>
    <div>${passenger.name || passenger.passenger_name || 'N/A'}</div>
    <div class="small-muted">${passenger.email || passenger.passenger_email || ''}</div>
  `;

  const right = document.createElement('div');
  right.innerHTML = `
    <div class="small-muted">Flight</div>
    <div style="font-weight:700; margin-bottom:8px;">${flight.airline_name || flight.airline || flight.flight_number || 'N/A'}</div>
    <div class="small-muted">Route</div>
    <div>${(flight.origin || '')} → ${(flight.destination || '')}</div>
    <div class="small-muted" style="margin-top:8px;">Seats</div>
    <div>${seats}</div>
    <div class="small-muted" style="margin-top:8px;">Price</div>
    <div>$${price}</div>
  `;

  html.appendChild(left);
  html.appendChild(right);

  receiptContainer.innerHTML = '';
  receiptContainer.appendChild(html);

  // Store raw data for download
  downloadBtn.style.display = 'inline-block';
  downloadBtn.dataset.payload = JSON.stringify(data, null, 2);
}

async function loadReceipt() {
  if (!pnr) {
    receiptContainer.innerHTML = `<div class="error">Missing PNR in URL.</div>`;
    return;
  }
  try {
    const data = await getReceipt(pnr);
    renderReceipt(data);
  } catch (err) {
    console.error(err);
    const text = err && err.body && err.body.message ? err.body.message : (err.body || err.message || 'Failed to load receipt.');
    receiptContainer.innerHTML = `<div class="error">Error: ${text}</div>`;
  }
}

downloadBtn.addEventListener('click', () => {
  const payload = downloadBtn.dataset.payload;
  if (!payload) return;
  const blob = new Blob([payload], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `receipt_${pnr || 'booking'}.json`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
});

loadReceipt();