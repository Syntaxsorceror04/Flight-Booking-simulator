// js/booking.js
import { reserveSeats } from './api.js';

const params = new URLSearchParams(window.location.search);
const flightId = params.get('flight_id');

const flightSummaryEl = document.getElementById('flightSummary');
const sideDetailsEl = document.getElementById('sideDetails');
const bookingForm = document.getElementById('bookingForm');
const passengerNameInput = document.getElementById('passengerName');
const passengerEmailInput = document.getElementById('passengerEmail');
const seatsInput = document.getElementById('seats');
const bookingMessage = document.getElementById('bookingMessage');
const reserveBtn = document.getElementById('reserveBtn');

function showMessage(text, type='error') {
  bookingMessage.innerHTML = text ? `<div class="${type === 'error' ? 'error' : 'success'}">${text}</div>` : '';
}

if (!flightId) {
  flightSummaryEl.innerHTML = `<div class="error">Missing flight_id in URL. Go back to search and select a flight.</div>`;
  bookingForm.style.display = 'none';
} else {
  // Populate summary from query params (we expect search page to pass details)
  const airline = params.get('airline') || '';
  const flight_number = params.get('flight_number') || '';
  const origin = params.get('origin') || '';
  const destination = params.get('destination') || '';
  const departure_time = params.get('departure_time') || '';
  const arrival_time = params.get('arrival_time') || '';
  const price = params.get('price') || '';
  const available_seats = params.get('available_seats') || '';

  flightSummaryEl.innerHTML = `
    <div>
      <div class="small-muted">Flight</div>
      <div class="route">${airline} • ${flight_number}</div>
      <div class="small-muted">${origin} → ${destination}</div>
      <div class="small-muted">${departure_time} → ${arrival_time}</div>
    </div>
    <div style="text-align:right;">
      <div class="small-muted">Price</div>
      <div class="price">$${price}</div>
      <div class="small-muted">${available_seats} seats left</div>
    </div>
  `;

  sideDetailsEl.innerHTML = `
    <div><strong>Flight ID:</strong> ${flightId}</div>
    <div><strong>Airline:</strong> ${airline}</div>
    <div><strong>Route:</strong> ${origin} → ${destination}</div>
    <div><strong>Departure:</strong> ${departure_time}</div>
  `;
}

// Validate and submit reservation
bookingForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  showMessage('', '');
  reserveBtn.disabled = true;

  const passenger_name = passengerNameInput.value.trim();
  const passenger_email = passengerEmailInput.value.trim();
  const seats_booked = parseInt(seatsInput.value, 10);

  if (!passenger_name) {
    showMessage('Passenger name is required.', 'error');
    reserveBtn.disabled = false;
    return;
  }
  if (!passenger_email || !/^\S+@\S+\.\S+$/.test(passenger_email)) {
    showMessage('A valid passenger email is required.', 'error');
    reserveBtn.disabled = false;
    return;
  }
  if (!seats_booked || seats_booked < 1) {
    showMessage('Seats to book must be at least 1.', 'error');
    reserveBtn.disabled = false;
    return;
  }

  try {
    const payload = {
      flight_id: Number(flightId),
      passenger_name,
      passenger_email,
      seats_booked
    };
    const res = await reserveSeats(payload);
    // Expecting { booking_id, status }
    if (!res || !res.booking_id) {
      throw new Error('Invalid response from server.');
    }
    // Compute total price if price available
    const unitPrice = parseFloat(params.get('price') || '0');
    const totalPrice = (unitPrice * seats_booked).toFixed(2);

    // Redirect to payment with booking_id and summary in query
    const q = new URLSearchParams({
      booking_id: res.booking_id,
      passenger_name,
      passenger_email,
      seats_booked: seats_booked,
      total_price: totalPrice,
      flight_id: flightId,
      airline: params.get('airline') || '',
      flight_number: params.get('flight_number') || '',
      origin: params.get('origin') || '',
      destination: params.get('destination') || '',
      departure_time: params.get('departure_time') || ''
    });
    window.location.href = `payment.html?${q.toString()}`;
  } catch (err) {
    console.error(err);
    const text = err && err.body && err.body.message ? err.body.message : (err.body || err.message || 'Reservation failed.');
    showMessage(`Error: ${text}`, 'error');
    reserveBtn.disabled = false;
  }
});