// js/search.js
import { searchFlights } from './api.js';

const form = document.getElementById('searchForm');
const originInput = document.getElementById('origin');
const destinationInput = document.getElementById('destination');
const dateInput = document.getElementById('date');
const resultsEl = document.getElementById('results');
const messageEl = document.getElementById('message');
const clearBtn = document.getElementById('clearBtn');

function showMessage(text, type = 'error') {
  if (!text) {
    messageEl.innerHTML = '';
    return;
  }
  messageEl.innerHTML = `<div class="${type === 'error' ? 'error' : 'success'}">${text}</div>`;
}

function formatTimeRange(dep, arr) {
  return `${dep} → ${arr}`;
}

function createFlightCard(f) {
  const card = document.createElement('div');
  card.className = 'card flight-card';

  const left = document.createElement('div');
  left.className = 'flight-left';

  const badge = document.createElement('div');
  badge.className = 'airline-badge';
  badge.textContent = (f.airline_name || '').slice(0,2).toUpperCase();

  const info = document.createElement('div');
  info.className = 'flight-info';

  const route = document.createElement('div');
  route.className = 'route';
  route.textContent = `${f.airline_name} • ${f.flight_number} — ${f.origin} → ${f.destination}`;

  const times = document.createElement('div');
  times.className = 'times';
  times.textContent = `${formatTimeRange(f.departure_time, f.arrival_time)}`;

  info.appendChild(route);
  info.appendChild(times);

  left.appendChild(badge);
  left.appendChild(info);

  const right = document.createElement('div');
  right.className = 'flight-right';

  const price = document.createElement('div');
  price.className = 'price';
  price.textContent = `$${f.current_price}`;

  const seats = document.createElement('div');
  seats.className = 'seats';
  seats.textContent = `${f.available_seats} seats left`;

  const btn = document.createElement('button');
  btn.className = 'btn';
  btn.textContent = 'Book Flight';
  btn.addEventListener('click', () => {
    // Redirect to booking page with flight details encoded in query string
    const params = new URLSearchParams({
      flight_id: f.id,
      airline: f.airline_name,
      flight_number: f.flight_number,
      origin: f.origin,
      destination: f.destination,
      departure_time: f.departure_time,
      arrival_time: f.arrival_time,
      price: f.current_price,
      available_seats: f.available_seats
    });
    window.location.href = `booking.html?${params.toString()}`;
  });

  right.appendChild(price);
  right.appendChild(seats);
  right.appendChild(btn);

  card.appendChild(left);
  card.appendChild(right);

  return card;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  showMessage('', '');
  resultsEl.innerHTML = '';

  const origin = originInput.value.trim().toUpperCase();
  const destination = destinationInput.value.trim().toUpperCase();

  const date = dateInput.value;

  if (!origin || !destination || !date) {
    showMessage('Please fill origin, destination and date.', 'error');
    return;
  }

  try {
    const data = await searchFlights(origin, destination, date);
    if (!Array.isArray(data) || data.length === 0) {
      showMessage('No flights found for the selected route and date.', 'error');
      return;
    }
    // Render flights
    data.forEach(f => {
      const card = createFlightCard(f);
      resultsEl.appendChild(card);
    });
    showMessage(`Found ${data.length} flight(s).`, 'success');
  } catch (err) {
    console.error(err);
    const text = err && err.body && err.body.message ? err.body.message : (err.body || err.message || 'Failed to fetch flights.');
    showMessage(`Error: ${text}`, 'error');
  }
});

clearBtn.addEventListener('click', () => {
  originInput.value = '';
  destinationInput.value = '';
  dateInput.value = '';
  resultsEl.innerHTML = '';
  showMessage('', '');
});