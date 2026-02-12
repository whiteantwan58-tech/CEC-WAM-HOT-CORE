/**
 * Google Drive and AppSheet Export Module
 * Handles capturing screenshots from live feeds and exporting data
 * Integrates with Google Drive API and AppSheet for seamless access
 */

class GoogleDriveExporter {
  constructor() {
    this.isAuthenticated = false;
    this.gapiLoaded = false;
    this.accessToken = null;
    this.exports = [];
    this.maxExports = 100;
    
    // Google Drive API configuration (would need actual credentials)
    // To configure: Set environment variables GOOGLE_CLIENT_ID and GOOGLE_API_KEY
    // Obtain credentials from: https://console.cloud.google.com/apis/credentials
    this.config = {
      clientId: process.env.GOOGLE_CLIENT_ID || '', // Set via environment variable
      apiKey: process.env.GOOGLE_API_KEY || '', // Set via environment variable
      scopes: 'https://www.googleapis.com/auth/drive.file',
      discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/drive/v3/rest']
    };
    
    this.init();
  }

  init() {
    // Listen for export events from other modules
    window.addEventListener('screenshotCaptured', (e) => this.handleScreenshot(e.detail));
    window.addEventListener('alertsExported', (e) => this.handleAlertExport(e.detail));
    window.addEventListener('newCrimeAlert', (e) => this.logCrimeAlert(e.detail));
    
    // Initialize export history
    this.loadExportHistory();
    
    // Create export UI
    this.createExportPanel();
  }

  createExportPanel() {
    // Create a floating export panel
    const panel = document.createElement('div');
    panel.id = 'exportPanel';
    panel.className = 'export-panel hidden';
    panel.innerHTML = `
      <div class="export-panel-header">
        <h3>📤 Export & Backup</h3>
        <button class="close-btn" id="closeExportPanel">×</button>
      </div>
      <div class="export-panel-body">
        <div class="export-section">
          <h4>Export Options</h4>
          <div class="export-buttons">
            <button class="export-btn" id="exportScreenshot">
              📸 Capture Screenshot
            </button>
            <button class="export-btn" id="exportCrimeData">
              🚨 Export Crime Data
            </button>
            <button class="export-btn" id="exportStarData">
              ⭐ Export Star Map Data
            </button>
            <button class="export-btn" id="exportAllData">
              💾 Export All Data
            </button>
          </div>
        </div>

        <div class="export-section">
          <h4>Integration Status</h4>
          <div class="integration-status">
            <div class="status-item">
              <span class="status-label">Google Drive:</span>
              <span class="status-value" id="driveStatus">Not Connected</span>
              <button class="connect-btn" id="connectDrive">Connect</button>
            </div>
            <div class="status-item">
              <span class="status-label">AppSheet:</span>
              <span class="status-value" id="appsheetStatus">Ready</span>
              <button class="connect-btn" id="openAppSheet">Open</button>
            </div>
          </div>
        </div>

        <div class="export-section">
          <h4>Export History</h4>
          <div class="export-history" id="exportHistory">
            <div class="no-exports">No exports yet</div>
          </div>
        </div>

        <div class="export-section">
          <h4>Auto-Export Settings</h4>
          <div class="auto-export-settings">
            <label class="setting-label">
              <input type="checkbox" id="autoExportScreenshots">
              Auto-export screenshots
            </label>
            <label class="setting-label">
              <input type="checkbox" id="autoExportCrimeData">
              Auto-export crime alerts
            </label>
            <label class="setting-label">
              <input type="checkbox" id="syncToAppSheet">
              Sync to AppSheet
            </label>
            <div class="setting-item">
              <label>Export Interval (minutes):</label>
              <input type="number" id="exportInterval" value="30" min="5" max="1440">
            </div>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(panel);

    // Add floating action button to open panel
    const fab = document.createElement('button');
    fab.id = 'exportFAB';
    fab.className = 'export-fab';
    fab.innerHTML = '📤';
    fab.title = 'Export & Backup';
    fab.addEventListener('click', () => this.toggleExportPanel());
    document.body.appendChild(fab);

    // Attach event listeners
    document.getElementById('closeExportPanel').addEventListener('click', () => this.toggleExportPanel());
    document.getElementById('exportScreenshot').addEventListener('click', () => this.captureAndExport());
    document.getElementById('exportCrimeData').addEventListener('click', () => this.exportCrimeData());
    document.getElementById('exportStarData').addEventListener('click', () => this.exportStarData());
    document.getElementById('exportAllData').addEventListener('click', () => this.exportAllData());
    document.getElementById('connectDrive').addEventListener('click', () => this.connectGoogleDrive());
    document.getElementById('openAppSheet').addEventListener('click', () => this.openAppSheet());
  }

  toggleExportPanel() {
    const panel = document.getElementById('exportPanel');
    panel.classList.toggle('hidden');
  }

  handleScreenshot(data) {
    // Store screenshot data
    const exportRecord = {
      id: `export-${Date.now()}`,
      type: 'screenshot',
      timestamp: data.timestamp || new Date().toISOString(),
      source: data.feedName || 'Unknown',
      data: data.dataUrl,
      status: 'local',
      size: this.calculateSize(data.dataUrl)
    };

    this.exports.unshift(exportRecord);
    this.trimExports();
    this.updateExportHistory();
    this.saveExportHistory();

    // Check if auto-export is enabled
    if (document.getElementById('autoExportScreenshots')?.checked) {
      this.uploadToGoogleDrive(exportRecord);
    }
  }

  handleAlertExport(data) {
    const exportRecord = {
      id: `export-${Date.now()}`,
      type: 'crime-data',
      timestamp: data.timestamp || new Date().toISOString(),
      count: data.count,
      data: data.data,
      status: 'local',
      size: this.calculateSize(data.data)
    };

    this.exports.unshift(exportRecord);
    this.trimExports();
    this.updateExportHistory();
    this.saveExportHistory();

    if (document.getElementById('autoExportCrimeData')?.checked) {
      this.uploadToGoogleDrive(exportRecord);
    }
  }

  logCrimeAlert(alert) {
    // Log individual crime alerts for AppSheet sync
    const logRecord = {
      id: alert.id,
      timestamp: alert.timestamp.toISOString(),
      type: alert.type,
      severity: alert.severity,
      title: alert.title,
      location: alert.location,
      description: alert.description
    };

    // Store in local storage for AppSheet sync
    const logs = this.getCrimeLogs();
    logs.unshift(logRecord);
    localStorage.setItem('crimeAlertLogs', JSON.stringify(logs.slice(0, 500)));

    if (document.getElementById('syncToAppSheet')?.checked) {
      this.syncToAppSheet(logRecord);
    }
  }

  getCrimeLogs() {
    try {
      return JSON.parse(localStorage.getItem('crimeAlertLogs') || '[]');
    } catch {
      return [];
    }
  }

  captureAndExport() {
    // Trigger screenshot capture from all available feeds
    const event = new CustomEvent('captureScreenshotRequest');
    window.dispatchEvent(event);
    
    // Show feedback
    this.showToast('Screenshot capture initiated', 'info');
  }

  exportCrimeData() {
    const event = new CustomEvent('exportCrimeDataRequest');
    window.dispatchEvent(event);
    
    this.showToast('Crime data export initiated', 'info');
  }

  exportStarData() {
    // Export current star map state
    const starData = {
      timestamp: new Date().toISOString(),
      constellations: [], // Would be populated by star map module
      celestialBodies: []
    };

    const json = JSON.stringify(starData, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `starmap-data-${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);

    this.showToast('Star map data exported', 'success');
  }

  async exportAllData() {
    this.showToast('Exporting all data...', 'info');

    // Collect all data
    const allData = {
      timestamp: new Date().toISOString(),
      screenshots: this.exports.filter(e => e.type === 'screenshot').length,
      crimeData: this.getCrimeLogs(),
      starMapData: {}, // Would be populated
      exportHistory: this.exports
    };

    const json = JSON.stringify(allData, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `cec-wam-export-${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);

    this.showToast('All data exported successfully', 'success');
  }

  async connectGoogleDrive() {
    // In a real implementation, this would initialize Google API
    this.showToast('Google Drive connection requires API credentials', 'warning');
    
    // Simulated connection
    document.getElementById('driveStatus').textContent = 'Connected (Demo)';
    document.getElementById('driveStatus').style.color = '#00ff88';
    
    // Would implement actual OAuth flow here
    // gapi.load('client:auth2', () => this.initGoogleAPI());
  }

  async uploadToGoogleDrive(exportRecord) {
    if (!this.isAuthenticated) {
      this.showToast('Please connect to Google Drive first', 'warning');
      return;
    }

    // Simulate upload (real implementation would use Google Drive API)
    exportRecord.status = 'uploading';
    this.updateExportHistory();

    setTimeout(() => {
      exportRecord.status = 'uploaded';
      exportRecord.driveId = `drive-${Date.now()}`;
      this.updateExportHistory();
      this.showToast(`${exportRecord.type} uploaded to Google Drive`, 'success');
    }, 2000);
  }

  openAppSheet() {
    // Open AppSheet URL (would be configured with actual AppSheet app)
    const appsheetUrl = 'https://www.appsheet.com/'; // Placeholder
    window.open(appsheetUrl, '_blank');
    this.showToast('Opening AppSheet...', 'info');
  }

  async syncToAppSheet(data) {
    // Simulate AppSheet sync (real implementation would use AppSheet API)
    console.log('Syncing to AppSheet:', data);
    
    // In production, would POST to AppSheet webhook or API
    // await fetch(appsheetWebhookUrl, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify(data)
    // });
  }

  updateExportHistory() {
    const historyContainer = document.getElementById('exportHistory');
    
    if (this.exports.length === 0) {
      historyContainer.innerHTML = '<div class="no-exports">No exports yet</div>';
      return;
    }

    historyContainer.innerHTML = this.exports.slice(0, 10).map(exp => `
      <div class="export-item">
        <div class="export-icon">${this.getExportIcon(exp.type)}</div>
        <div class="export-info">
          <div class="export-title">${exp.type}</div>
          <div class="export-meta">
            ${new Date(exp.timestamp).toLocaleString()} • ${exp.size}
          </div>
        </div>
        <div class="export-status ${exp.status}">${exp.status}</div>
      </div>
    `).join('');
  }

  getExportIcon(type) {
    const icons = {
      'screenshot': '📸',
      'crime-data': '🚨',
      'star-data': '⭐',
      'all-data': '💾'
    };
    return icons[type] || '📄';
  }

  calculateSize(data) {
    if (typeof data === 'string') {
      const bytes = new Blob([data]).size;
      if (bytes < 1024) return `${bytes} B`;
      if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
      return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    }
    return 'Unknown';
  }

  trimExports() {
    if (this.exports.length > this.maxExports) {
      this.exports = this.exports.slice(0, this.maxExports);
    }
  }

  saveExportHistory() {
    try {
      // Save only metadata, not actual data
      const metadata = this.exports.map(exp => ({
        id: exp.id,
        type: exp.type,
        timestamp: exp.timestamp,
        status: exp.status,
        size: exp.size
      }));
      localStorage.setItem('exportHistory', JSON.stringify(metadata));
    } catch (error) {
      console.error('Failed to save export history:', error);
    }
  }

  loadExportHistory() {
    try {
      const metadata = JSON.parse(localStorage.getItem('exportHistory') || '[]');
      this.exports = metadata;
    } catch (error) {
      console.error('Failed to load export history:', error);
    }
  }

  showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast-notification ${type}`;
    toast.innerHTML = `
      <div class="toast-icon">${this.getToastIcon(type)}</div>
      <div class="toast-message">${message}</div>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
      toast.style.animation = 'slideOut 0.3s ease-out forwards';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  getToastIcon(type) {
    const icons = {
      'info': 'ℹ️',
      'success': '✅',
      'warning': '⚠️',
      'error': '❌'
    };
    return icons[type] || 'ℹ️';
  }

  // Public methods
  getExportCount() {
    return this.exports.length;
  }

  getExportById(id) {
    return this.exports.find(e => e.id === id);
  }

  clearExportHistory() {
    this.exports = [];
    this.saveExportHistory();
    this.updateExportHistory();
    this.showToast('Export history cleared', 'info');
  }
}

// Auto-initialize when DOM is ready
if (typeof window !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      window.googleDriveExporter = new GoogleDriveExporter();
    });
  } else {
    window.googleDriveExporter = new GoogleDriveExporter();
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = GoogleDriveExporter;
}
