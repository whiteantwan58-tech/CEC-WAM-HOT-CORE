// app.js - CEC-WAM LIVE core logic
// Requires: Chart.js, localForage

// Setup localForage store
localforage.config({ name: 'cec_wam_store' });
const DATA_KEY = 'cec_logs_v1';
const META_KEY = 'cec_meta_v1';

// UI refs
const sheetUrlInput = document.getElementById('sheet-url');
const linkBtn = document.getElementById('link-sheet');
const unlinkBtn = document.getElementById('unlink-sheet');
const fetchNowBtn = document.getElementById('fetch-now');
const importFileInput = document.getElementById('file-input');
const importBtn = document.getElementById('import-btn');
const exportBtn = document.getElementById('export-btn');
const startMicBtn = document.getElementById('start-mic');
const speakBtn = document.getElementById('speak-sample');
const logBox = document.getElementById('log-box');
const lastSync = document.getElementById('last-sync');
const statusEl = document.getElementById('status');
const pinInput = document.getElementById('pin-input');
const setPinBtn = document.getElementById('set-pin');

let cachedUrl = localStorage.getItem('cec_sheet_url') || '';
sheetUrlInput.value = cachedUrl;

// Simple charts
const kpiCtx = document.getElementById('kpichart').getContext('2d');
const seriesCtx = document.getElementById('serieschart').getContext('2d');
let kpiChart, seriesChart;

// Initialize charts
function initCharts() {
  kpiChart = new Chart(kpiCtx, {
    type: 'doughnut',
    data: { labels: ['Liquid', 'DarkEnergy', 'Other'], datasets: [{ data: [60, 25, 15], backgroundColor: ['#00f3ff','#bc13fe','#ffd700'] }] },
    options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
  });

  seriesChart = new Chart(seriesCtx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Liquidity (M)', data: [], borderColor: '#00f3ff', fill: false }] },
    options: { responsive: true, maintainAspectRatio: false }
  });
}

// Helpers
function appendLog(msg, cls='') {
  const ts = new Date().toISOString();
  const row = document.createElement('div');
  row.innerHTML = `<span class="text-gray-600">[${ts}]</span> ${msg}`;
  if (cls) row.classList.add(cls);
  logBox.appendChild(row);
  logBox.scrollTop = logBox.scrollHeight;
  saveLogToStore({ ts, msg });
}

async function saveLogToStore(entry) {
  const data = (await localforage.getItem(DATA_KEY)) || [];
  data.push(entry);
  await localforage.setItem(DATA_KEY, data);
}

async function loadStoredLogs() {
  return (await localforage.getItem(DATA_KEY)) || [];
}

// CSV parsing (very small)
function csvToRows(csvText) {
  const lines = csvText.trim().split(/\r?\n/);
  const headers = lines.shift().split(',').map(h => h.trim());
  return lines.map(l => {
    const cols = l.split(',').map(c => c.trim());
    const obj = {};
    headers.forEach((h, i) => obj[h] = cols[i] || '');
    return obj;
  });
}

// Merge data into logs with timestamp
async function mergeRecords(records, source='remote') {
  const now = new Date().toISOString();
  for (const rec of records) {
    const msg = JSON.stringify(rec);
    await saveLogToStore({ ts: now, source, data: rec });
    appendLog(`${source}: ${msg}`);
  }
  updateChartsFromStorage();
}

// Fetch Google sheet CSV url
async function fetchSheetAndMerge(url) {
  try {
    statusEl.innerText = 'Fetching...';
    const res = await fetch(url, { cache: 'no-store' });
    if (!res.ok) throw new Error('Fetch failed ' + res.status);
    const text = await res.text();
    const rows = csvToRows(text);
    await mergeRecords(rows, 'sheet');
    statusEl.innerText = 'Last fetch OK';
    localforage.setItem(META_KEY, { lastSync: new Date().toISOString(), source: url });
    lastSync.innerText = 'Last sync: ' + new Date().toLocaleString();
  } catch (e) {
    console.error(e);
    appendLog('Fetch error: ' + e.message, 'text-red-400');
    statusEl.innerText = 'Fetch error';
  }
}

// Import local CSV/XLSX
function handleImportFile(file) {
  const reader = new FileReader();
  reader.onload = async (ev) => {
    const text = ev.target.result;
    // Try CSV parse; advanced: accept XLSX with a library (not included)
    const rows = csvToRows(text);
    await mergeRecords(rows, 'import');
    appendLog('Imported file: ' + file.name);
  };
  reader.readAsText(file);
}

// Build charts from stored logs (simple example)
async function updateChartsFromStorage() {
  const logs = await loadStoredLogs();
  // For demo, try to read numeric "Liquidity" or "Value" fields if present
  const labels = [];
  const series = [];
  for (let i = Math.max(0, logs.length - 50); i < logs.length; i++) {
    const rec = logs[i];
    labels.push(new Date(rec.ts).toLocaleTimeString());
    // best-effort: find a numeric field in rec.data
    let val = null;
    if (rec.data) {
      for (const k of Object.keys(rec.data)) {
        const v = rec.data[k];
        if (!isNaN(parseFloat(v))) { val = parseFloat(v); break; }
      }
    }
    series.push(val || 0);
  }
  seriesChart.data.labels = labels;
  seriesChart.data.datasets[0].data = series;
  seriesChart.update();

  // Update KPI chart with last-known values
  let liquid = 60, dark = 25, other = 15;
  // naive attempt to compute from last record
  const lastRec = logs[logs.length - 1];
  if (lastRec && lastRec.data) {
    if (lastRec.data.Liquidity) {
      liquid = Math.min(100, parseFloat(lastRec.data.Liquidity) / 1000000 || 60);
    }
  }
  kpiChart.data.datasets[0].data = [liquid, dark, other];
  kpiChart.update();
}

// Voice: Web Speech API (speech recognition)
let recognition;
if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SR();
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onresult = async (e) => {
    const text = e.results[0][0].transcript;
    appendLog('EVE HEI (voice input): ' + text);
    // Simple TTS reply:
    speak('Heard: ' + text);
    // Add as a log entry
    await saveLogToStore({ ts: new Date().toISOString(), source: 'voice', data: { note: text }});
    updateChartsFromStorage();
  };
  recognition.onerror = (ev) => { appendLog('Voice error: ' + ev.error); };
} else {
  startMicBtn.disabled = true;
  appendLog('Voice not supported in this browser.');
}

function speak(text) {
  if ('speechSynthesis' in window) {
    const ut = new SpeechSynthesisUtterance(text);
    ut.lang = 'en-US';
    window.speechSynthesis.speak(ut);
  }
}

// PIN handling (stores salted hash locally)
async function setPin(pin) {
  if (!pin || pin.length < 4) { alert('Use a longer PIN'); return; }
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const enc = new TextEncoder();
  const data = enc.encode(pin + Array.from(salt).join('-'));
  const hash = await crypto.subtle.digest('SHA-256', data);
  const h = Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2,'0')).join('');
  await localforage.setItem('pin_hash', { hash: h, salt: Array.from(salt) });
  appendLog('Local PIN set (device only).');
}

// Export logs to CSV
async function exportLogs() {
  const logs = await loadStoredLogs();
  let csv = 'timestamp,source,json\n';
  for (const l of logs) {
    csv += `${l.ts},${l.source || ''},"${JSON.stringify(l.data || l.msg).replace(/"/g,'""')}"\n`;
  }
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href = url; a.download = 'cec_logs_export.csv'; a.click();
  URL.revokeObjectURL(url);
}

// Wire UI
linkBtn.addEventListener('click', () => {
  const url = sheetUrlInput.value.trim();
  if (!url) return alert('Paste the published CSV URL from Google Sheets.');
  localStorage.setItem('cec_sheet_url', url);
  cachedUrl = url;
  appendLog('Linked sheet URL (will poll).');
  fetchSheetAndMerge(url);
});

unlinkBtn.addEventListener('click', () => {
  localStorage.removeItem('cec_sheet_url');
  sheetUrlInput.value = '';
  cachedUrl = '';
  appendLog('Unlinked sheet URL.');
});

fetchNowBtn.addEventListener('click', () => {
  const url = sheetUrlInput.value.trim() || cachedUrl;
  if (!url) return alert('No sheet URL linked.');
  fetchSheetAndMerge(url);
});

importBtn.addEventListener('click', () => {
  const f = importFileInput.files[0];
  if (!f) return alert('Choose a file first.');
  handleImportFile(f);
});

exportBtn.addEventListener('click', () => exportLogs());

startMicBtn.addEventListener('click', () => {
  if (!recognition) return alert('SpeechRecognition not available.');
  recognition.start();
});

speakBtn.addEventListener('click', () => speak('Hello, E V E. System ready.'));

setPinBtn.addEventListener('click', () => {
  const p = pinInput.value.trim();
  setPin(p);
  pinInput.value = '';
});

// Auto init
(async () => {
  initCharts();
  // Load stored logs into log box
  const logs = await loadStoredLogs();
  logs.slice(-200).forEach(l => {
    appendLog(`${l.source || 'local'}: ${JSON.stringify(l.data || l.msg)}`);
  });
  // If a sheet URL is saved, schedule periodic fetch
  if (cachedUrl) {
    appendLog('Auto-fetch scheduled for linked CSV: ' + cachedUrl);
    fetchSheetAndMerge(cachedUrl);
    setInterval(() => {
      if (cachedUrl) fetchSheetAndMerge(cachedUrl);
    }, 60_000); // every 60s (adjustable)
  }
  updateChartsFromStorage();
})();
