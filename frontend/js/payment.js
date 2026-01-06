// js/payment.js
import { makePayment } from './api.js';

const params = new URLSearchParams(window.location.search);
const bookingId = params.get('booking_id');

const bookingSummaryEl = document.getElementById('bookingSummary');
const sideSummaryEl = document.getElementById('sideSummary');
const paymentForm = document.getElementById('paymentForm');
const paymentMethodSelect = document.getElementById('paymentMethod');
const paymentFields = document.getElementById('paymentFields');
const paymentMessage = document.getElementById('paymentMessage');
const payBtn = document.getElementById('payBtn');
const cancelLink = document.getElementById('cancelLink');

function showMessage(text, type='error') {
  paymentMessage.innerHTML = text ? `<div class="${type === 'error' ? 'error' : 'success'}">${text}</div>` : '';
}

if (!bookingId) {
  bookingSummaryEl.innerHTML = `<div class="error">Missing booking_id in URL. Cannot proceed to payment.</div>`;
  paymentForm.style.display = 'none';
} else {
  const passenger_name = params.get('passenger_name') || '';
  const passenger_email = params.get('passenger_email') || '';
  const seats_booked = params.get('seats_booked') || '1';
  const total_price = params.get('total_price') || '0.00';
  const airline = params.get('airline') || '';
  const flight_number = params.get('flight_number') || '';
  const origin = params.get('origin') || '';
  const destination = params.get('destination') || '';
  const departure_time = params.get('departure_time') || '';

  bookingSummaryEl.innerHTML = `
    <div>
      <div class="small-muted">Booking</div>
      <div class="route">${airline} • ${flight_number}</div>
      <div class="small-muted">${origin} → ${destination}</div>
      <div class="small-muted">${departure_time}</div>
    </div>
    <div style="text-align:right;">
      <div class="small-muted">Passenger</div>
      <div>${passenger_name}</div>
      <div class="small-muted">${passenger_email}</div>
      <div style="margin-top:8px;" class="small-muted">Seats: ${seats_booked}</div>
      <div class="price" style="margin-top:8px;">Total: $${total_price}</div>
    </div>
  `;

  sideSummaryEl.innerHTML = `
    <div><strong>Booking ID:</strong> ${bookingId}</div>
    <div><strong>Seats:</strong> ${seats_booked}</div>
    <div><strong>Total:</strong> $${total_price}</div>
  `;

  cancelLink.href = `booking.html?flight_id=${encodeURIComponent(params.get('flight_id') || '')}`;
}

// Dynamic payment fields (simple simulation)
paymentMethodSelect.addEventListener('change', () => {
  const method = paymentMethodSelect.value;
  paymentFields.innerHTML = '';
  if (method === 'card') {
    paymentFields.innerHTML = `
      <div class="field"><label class="small">Card number</label><input id="cardNumber" class="input" type="text" inputmode="numeric" maxlength="19" required /></div>
      <div class="field"><label class="small">Expiry (MM/YY)</label><input id="cardExpiry" class="input" type="text" maxlength="5" placeholder="MM/YY" required /></div>
      <div class="field"><label class="small">CVV</label><input id="cardCvv" class="input" type="password" maxlength="4" required /></div>
    `;
  } else if (method === 'netbanking') {
    paymentFields.innerHTML = `
      <div class="field"><label class="small">Bank</label><input id="bankName" class="input" type="text" required /></div>
      <div class="field"><label class="small">Transaction reference</label><input id="txnRef" class="input" type="text" required /></div>
    `;
  } else if (method === 'upi') {
    paymentFields.innerHTML = `
      <div class="field"><label class="small">UPI ID</label><input id="upiId" class="input" type="text" required /></div>
      <div class="field"><label class="small">UPI Transaction ref</label><input id="upiRef" class="input" type="text" required /></div>
    `;
  }
});

paymentForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  showMessage('', '');
  payBtn.disabled = true;

  const method = paymentMethodSelect.value;
  if (!method) {
    showMessage('Please select a payment method.', 'error');
    payBtn.disabled = false;
    return;
  }

  // Basic validation for dynamic fields
  const inputs = paymentForm.querySelectorAll('input');
  for (const inp of inputs) {
    if (inp.required && !inp.value.trim()) {
      showMessage('Please fill all required payment fields.', 'error');
      payBtn.disabled = false;
      return;
    }
  }

  // Prepare a minimal payment payload (simulation)
  const payload = {
    method,
    metadata: {}
  };

  // Collect some metadata for backend if needed
  if (method === 'card') {
    payload.metadata.card_last4 = (document.getElementById('cardNumber')?.value || '').slice(-4);
  } else if (method === 'netbanking') {
    payload.metadata.bank = document.getElementById('bankName')?.value || '';
  } else if (method === 'upi') {
    payload.metadata.upi = document.getElementById('upiId')?.value || '';
  }

  try {
    const res = await makePayment(bookingId, payload);
    // Expecting { status, pnr }
    if (!res || res.status !== 'success' || !res.pnr) {
      // If backend returns status but no pnr, show message
      const msg = res && res.status ? `Payment status: ${res.status}` : 'Payment failed or invalid response.';
      throw new Error(msg);
    }
    // Redirect to receipt
    window.location.href = `receipt.html?pnr=${encodeURIComponent(res.pnr)}`;
  } catch (err) {
    console.error(err);
    const text = err && err.body && err.body.message ? err.body.message : (err.body || err.message || 'Payment failed.');
    showMessage(`Error: ${text}`, 'error');
    payBtn.disabled = false;
  }
});rece