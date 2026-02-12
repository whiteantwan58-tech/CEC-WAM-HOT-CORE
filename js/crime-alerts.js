/**
 * Crime Alert and Police Scanner Integration Module
 * Embeds live crime alert feed and police scanner with alert notifications
 * Displays date, time, and location information for each alert
 */

class CrimeAlertSystem {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    if (!this.container) {
      console.error('Container element not found:', containerId);
      return;
    }
    
    this.alerts = [];
    this.maxAlerts = 50;
    this.updateInterval = 30000; // 30 seconds
    this.audioEnabled = false;
    this.notificationCount = 0;
    
    this.init();
  }

  init() {
    // Create alert system UI
    this.createUI();
    
    // Initialize with sample data (in production, this would fetch from actual APIs)
    this.loadInitialAlerts();
    
    // Start periodic updates
    this.startPeriodicUpdates();
    
    // Request notification permission
    this.requestNotificationPermission();
  }

  createUI() {
    this.container.innerHTML = `
      <div class="crime-alert-wrapper">
        <div class="alert-header">
          <div class="header-left">
            <h3 class="alert-title">🚨 Crime Alert Feed</h3>
            <span class="alert-subtitle">Federal Way, WA - Live Updates</span>
          </div>
          <div class="header-right">
            <button class="alert-btn" id="audioToggle" title="Toggle Alert Sound">
              🔇
            </button>
            <button class="alert-btn" id="refreshAlerts" title="Refresh Alerts">
              🔄
            </button>
            <button class="alert-btn" id="exportAlerts" title="Export Alerts">
              💾
            </button>
            <span class="alert-count" id="alertCount">0 Active</span>
          </div>
        </div>

        <div class="scanner-controls">
          <div class="scanner-status">
            <span class="scanner-indicator pulse-indicator"></span>
            <span>Scanner: <span id="scannerStatus">Active</span></span>
          </div>
          <div class="filter-controls">
            <select id="severityFilter" class="filter-select">
              <option value="all">All Severity</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
            <select id="typeFilter" class="filter-select">
              <option value="all">All Types</option>
              <option value="theft">Theft</option>
              <option value="assault">Assault</option>
              <option value="traffic">Traffic</option>
              <option value="suspicious">Suspicious Activity</option>
              <option value="other">Other</option>
            </select>
          </div>
        </div>

        <div class="alerts-container" id="alertsContainer">
          <div class="loading-spinner">
            <div class="spinner"></div>
            <p>Loading alerts...</p>
          </div>
        </div>

        <div class="alert-footer">
          <div class="footer-info">
            <span>Last Updated: <span id="lastUpdate">--:--:--</span></span>
            <span>Data Source: Federal Way Police Scanner</span>
          </div>
        </div>
      </div>
    `;

    // Attach event listeners
    document.getElementById('audioToggle').addEventListener('click', () => this.toggleAudio());
    document.getElementById('refreshAlerts').addEventListener('click', () => this.refreshAlerts());
    document.getElementById('exportAlerts').addEventListener('click', () => this.exportAlerts());
    document.getElementById('severityFilter').addEventListener('change', (e) => this.filterAlerts(e.target.value, 'severity'));
    document.getElementById('typeFilter').addEventListener('change', (e) => this.filterAlerts(e.target.value, 'type'));
  }

  loadInitialAlerts() {
    // Generate sample alerts (in production, fetch from actual crime data API)
    const alertTypes = ['theft', 'assault', 'traffic', 'suspicious', 'other'];
    const severities = ['critical', 'high', 'medium', 'low'];
    const locations = [
      'Main St & Pacific Hwy',
      'City Hall Area',
      'Transit Center',
      'Commons Mall',
      'Celebration Park',
      'Steel Lake Park',
      'Dash Point',
      'Twin Lakes'
    ];

    // Generate 15 initial alerts
    for (let i = 0; i < 15; i++) {
      const now = new Date();
      const alertTime = new Date(now - Math.random() * 3600000 * 24); // Random within last 24h
      
      this.alerts.push({
        id: `alert-${Date.now()}-${i}`,
        type: alertTypes[Math.floor(Math.random() * alertTypes.length)],
        severity: severities[Math.floor(Math.random() * severities.length)],
        title: this.generateAlertTitle(),
        location: locations[Math.floor(Math.random() * locations.length)],
        timestamp: alertTime,
        description: this.generateAlertDescription(),
        units: Math.floor(Math.random() * 3) + 1,
        status: Math.random() > 0.3 ? 'active' : 'resolved'
      });
    }

    // Sort by timestamp (newest first)
    this.alerts.sort((a, b) => b.timestamp - a.timestamp);
    
    // Render alerts
    this.renderAlerts();
    this.updateStats();
  }

  generateAlertTitle() {
    const titles = [
      'Vehicle Theft Reported',
      'Suspicious Activity',
      'Traffic Accident',
      'Assault in Progress',
      'Break-in Attempt',
      'Domestic Disturbance',
      'Welfare Check',
      'Noise Complaint',
      'Burglary Report',
      'Vandalism Incident'
    ];
    return titles[Math.floor(Math.random() * titles.length)];
  }

  generateAlertDescription() {
    const descriptions = [
      'Multiple units dispatched to scene',
      'Caller reported suspicious individual',
      'Minor injuries reported',
      'Officers investigating the area',
      'Witness statements being collected',
      'Backup requested',
      'Scene secured by officers',
      'Investigation ongoing'
    ];
    return descriptions[Math.floor(Math.random() * descriptions.length)];
  }

  renderAlerts(filteredAlerts = null) {
    const container = document.getElementById('alertsContainer');
    const alertsToRender = filteredAlerts || this.alerts;

    if (alertsToRender.length === 0) {
      container.innerHTML = '<div class="no-alerts">No alerts match the current filters</div>';
      return;
    }

    container.innerHTML = alertsToRender.map(alert => `
      <div class="alert-item ${alert.severity} ${alert.status}" data-id="${alert.id}">
        <div class="alert-item-header">
          <div class="alert-severity-badge ${alert.severity}">
            ${this.getSeverityIcon(alert.severity)} ${alert.severity.toUpperCase()}
          </div>
          <div class="alert-type-badge">${this.getTypeIcon(alert.type)} ${alert.type.toUpperCase()}</div>
          <div class="alert-status-badge ${alert.status}">${alert.status.toUpperCase()}</div>
        </div>
        <div class="alert-item-body">
          <h4 class="alert-item-title">${alert.title}</h4>
          <div class="alert-item-info">
            <div class="info-row">
              <span class="info-label">📍 Location:</span>
              <span class="info-value">${alert.location}</span>
            </div>
            <div class="info-row">
              <span class="info-label">🕐 Time:</span>
              <span class="info-value">${this.formatTimestamp(alert.timestamp)}</span>
            </div>
            <div class="info-row">
              <span class="info-label">👮 Units:</span>
              <span class="info-value">${alert.units} responding</span>
            </div>
          </div>
          <p class="alert-description">${alert.description}</p>
        </div>
        <div class="alert-item-footer">
          <span class="alert-id">ID: ${alert.id.slice(-8)}</span>
          <span class="alert-age">${this.getAlertAge(alert.timestamp)}</span>
        </div>
      </div>
    `).join('');
  }

  getSeverityIcon(severity) {
    const icons = {
      critical: '🔴',
      high: '🟠',
      medium: '🟡',
      low: '🟢'
    };
    return icons[severity] || '⚪';
  }

  getTypeIcon(type) {
    const icons = {
      theft: '🏪',
      assault: '⚠️',
      traffic: '🚗',
      suspicious: '👁️',
      other: '📋'
    };
    return icons[type] || '📋';
  }

  formatTimestamp(timestamp) {
    return timestamp.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  }

  getAlertAge(timestamp) {
    const now = new Date();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'Just now';
  }

  filterAlerts(value, filterType) {
    let filtered = this.alerts;

    const severityFilter = document.getElementById('severityFilter').value;
    const typeFilter = document.getElementById('typeFilter').value;

    if (severityFilter !== 'all') {
      filtered = filtered.filter(alert => alert.severity === severityFilter);
    }

    if (typeFilter !== 'all') {
      filtered = filtered.filter(alert => alert.type === typeFilter);
    }

    this.renderAlerts(filtered);
  }

  startPeriodicUpdates() {
    setInterval(() => {
      this.simulateNewAlert();
      this.updateStats();
    }, this.updateInterval);

    // Update timestamp every second
    setInterval(() => {
      const now = new Date();
      document.getElementById('lastUpdate').textContent = now.toLocaleTimeString();
    }, 1000);
  }

  simulateNewAlert() {
    // Simulate a new alert arriving (in production, this would poll actual API)
    if (Math.random() > 0.7) { // 30% chance of new alert
      const newAlert = {
        id: `alert-${Date.now()}`,
        type: ['theft', 'assault', 'traffic', 'suspicious', 'other'][Math.floor(Math.random() * 5)],
        severity: ['critical', 'high', 'medium', 'low'][Math.floor(Math.random() * 4)],
        title: this.generateAlertTitle(),
        location: ['Main St & Pacific Hwy', 'City Hall Area', 'Transit Center'][Math.floor(Math.random() * 3)],
        timestamp: new Date(),
        description: this.generateAlertDescription(),
        units: Math.floor(Math.random() * 3) + 1,
        status: 'active'
      };

      this.alerts.unshift(newAlert);
      
      // Keep only max alerts
      if (this.alerts.length > this.maxAlerts) {
        this.alerts.pop();
      }

      this.renderAlerts();
      this.showNotification(newAlert);
      
      if (this.audioEnabled) {
        this.playAlertSound();
      }

      // Dispatch event
      window.dispatchEvent(new CustomEvent('newCrimeAlert', {
        detail: newAlert
      }));
    }
  }

  updateStats() {
    const activeAlerts = this.alerts.filter(a => a.status === 'active').length;
    document.getElementById('alertCount').textContent = `${activeAlerts} Active`;
  }

  showNotification(alert) {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification('🚨 New Crime Alert', {
        body: `${alert.title} - ${alert.location}`,
        icon: '/icon.png',
        badge: '/badge.png',
        tag: alert.id
      });
    }

    // Visual notification in UI
    this.notificationCount++;
    const notification = document.createElement('div');
    notification.className = 'toast-notification';
    notification.innerHTML = `
      <div class="toast-icon">🚨</div>
      <div class="toast-content">
        <div class="toast-title">New Alert</div>
        <div class="toast-message">${alert.title}</div>
      </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.style.animation = 'slideOut 0.3s ease-out forwards';
      setTimeout(() => notification.remove(), 300);
    }, 5000);
  }

  playAlertSound() {
    // Create and play a simple alert tone
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.value = 800;
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.5);
  }

  toggleAudio() {
    this.audioEnabled = !this.audioEnabled;
    const btn = document.getElementById('audioToggle');
    btn.textContent = this.audioEnabled ? '🔊' : '🔇';
    btn.title = this.audioEnabled ? 'Mute Alert Sound' : 'Enable Alert Sound';
  }

  refreshAlerts() {
    document.getElementById('refreshAlerts').textContent = '⟳';
    this.simulateNewAlert();
    setTimeout(() => {
      document.getElementById('refreshAlerts').textContent = '🔄';
    }, 1000);
  }

  exportAlerts() {
    // Export alerts to CSV
    const csv = this.convertToCSV();
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `crime-alerts-${Date.now()}.csv`;
    link.click();
    URL.revokeObjectURL(url);

    // Dispatch event for external handling (e.g., Google Drive upload)
    window.dispatchEvent(new CustomEvent('alertsExported', {
      detail: {
        data: csv,
        timestamp: new Date().toISOString(),
        count: this.alerts.length
      }
    }));
  }

  convertToCSV() {
    const headers = ['ID', 'Timestamp', 'Type', 'Severity', 'Title', 'Location', 'Description', 'Units', 'Status'];
    const rows = this.alerts.map(alert => [
      alert.id,
      alert.timestamp.toISOString(),
      alert.type,
      alert.severity,
      alert.title,
      alert.location,
      alert.description,
      alert.units,
      alert.status
    ]);

    return [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n');
  }

  async requestNotificationPermission() {
    if ('Notification' in window && Notification.permission === 'default') {
      await Notification.requestPermission();
    }
  }

  destroy() {
    // Cleanup
    this.alerts = [];
  }

  // Public methods
  getActiveAlerts() {
    return this.alerts.filter(a => a.status === 'active');
  }

  getAlertById(id) {
    return this.alerts.find(a => a.id === id);
  }

  getTotalAlerts() {
    return this.alerts.length;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CrimeAlertSystem;
}
