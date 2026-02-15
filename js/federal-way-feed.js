/**
 * Federal Way Live Feed Integration Module
 * Streams live video feed from Federal Way cameras in HD color
 * Note: This module provides a framework for live feed integration
 * Actual feed URLs would need to be configured based on available camera APIs
 */

class FederalWayLiveFeed {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    if (!this.container) {
      console.error('Container element not found:', containerId);
      return;
    }
    
    this.videoElement = null;
    this.statusElement = null;
    this.feeds = [];
    this.currentFeedIndex = 0;
    this.isStreaming = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    
    this.init();
  }

  init() {
    // Create video container structure
    this.createVideoContainer();
    
    // Define available feeds (placeholder URLs - would need actual Federal Way camera feeds)
    this.feeds = [
      {
        name: 'Federal Way Main St',
        url: 'placeholder-feed-1',
        type: 'webcam',
        location: 'Main Street & Pacific Highway'
      },
      {
        name: 'Federal Way City Hall',
        url: 'placeholder-feed-2',
        type: 'webcam',
        location: 'City Hall Campus'
      },
      {
        name: 'Federal Way Transit Center',
        url: 'placeholder-feed-3',
        type: 'webcam',
        location: 'Transit Center Plaza'
      }
    ];
    
    // Initialize with placeholder content
    this.initializePlaceholder();
    
    // Auto-cycle feeds
    this.startFeedCycle();
  }

  createVideoContainer() {
    this.container.innerHTML = `
      <div class="live-feed-wrapper">
        <div class="feed-header">
          <div class="feed-info">
            <span class="feed-title" id="feedTitle">Federal Way Live Feed</span>
            <span class="feed-location" id="feedLocation">Loading...</span>
          </div>
          <div class="feed-controls">
            <button class="feed-btn" id="prevFeed" title="Previous Feed">◀</button>
            <button class="feed-btn" id="nextFeed" title="Next Feed">▶</button>
            <button class="feed-btn" id="captureBtn" title="Capture Screenshot">📷</button>
            <span class="live-indicator">
              <span class="pulse-dot"></span>
              <span>LIVE</span>
            </span>
          </div>
        </div>
        <div class="video-container" id="videoContainer">
          <video id="liveVideo" autoplay playsinline></video>
          <div class="video-overlay" id="videoOverlay">
            <div class="overlay-content">
              <div class="camera-icon">📹</div>
              <div class="overlay-text">Federal Way Live Camera Feed</div>
              <div class="overlay-subtext" id="overlayStatus">Initializing...</div>
            </div>
          </div>
        </div>
        <div class="feed-footer">
          <div class="timestamp" id="feedTimestamp">--:--:--</div>
          <div class="feed-quality">
            <span id="feedQuality">HD</span>
            <span id="feedResolution">1920x1080</span>
          </div>
        </div>
      </div>
    `;
    
    this.videoElement = document.getElementById('liveVideo');
    this.statusElement = document.getElementById('overlayStatus');
    
    // Attach event listeners
    document.getElementById('prevFeed').addEventListener('click', () => this.previousFeed());
    document.getElementById('nextFeed').addEventListener('click', () => this.nextFeed());
    document.getElementById('captureBtn').addEventListener('click', () => this.captureScreenshot());
    
    // Start timestamp update
    this.updateTimestamp();
  }

  initializePlaceholder() {
    // Since we don't have actual Federal Way camera feeds, show informative placeholder
    const overlay = document.getElementById('videoOverlay');
    const currentFeed = this.feeds[this.currentFeedIndex];
    
    document.getElementById('feedTitle').textContent = currentFeed.name;
    document.getElementById('feedLocation').textContent = currentFeed.location;
    
    this.statusElement.textContent = 'Live feed integration ready';
    
    // Create animated placeholder background
    this.createAnimatedPlaceholder();
  }

  createAnimatedPlaceholder() {
    const videoContainer = document.getElementById('videoContainer');
    
    // Add animated gradient background
    const canvas = document.createElement('canvas');
    canvas.id = 'placeholderCanvas';
    canvas.width = videoContainer.clientWidth;
    canvas.height = videoContainer.clientHeight;
    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.zIndex = '1';
    
    videoContainer.insertBefore(canvas, videoContainer.firstChild);
    
    const ctx = canvas.getContext('2d');
    let frame = 0;
    
    const animate = () => {
      frame++;
      
      // Create gradient animation
      const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
      const offset = (Math.sin(frame * 0.02) + 1) / 2;
      
      gradient.addColorStop(0, `rgba(14, 14, 27, ${0.9 + offset * 0.1})`);
      gradient.addColorStop(0.5, `rgba(26, 26, 46, ${0.85 + offset * 0.15})`);
      gradient.addColorStop(1, `rgba(14, 14, 27, ${0.9 + offset * 0.1})`);
      
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Add moving scan lines
      ctx.strokeStyle = 'rgba(0, 255, 224, 0.1)';
      ctx.lineWidth = 2;
      
      for (let i = 0; i < 5; i++) {
        const y = ((frame * 2 + i * 100) % (canvas.height + 100)) - 50;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
      }
      
      requestAnimationFrame(animate);
    };
    
    animate();
  }

  updateTimestamp() {
    setInterval(() => {
      const now = new Date();
      const timestamp = now.toLocaleTimeString('en-US', { 
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
      document.getElementById('feedTimestamp').textContent = timestamp;
    }, 1000);
  }

  startFeedCycle() {
    // Auto-cycle through feeds every 15 seconds
    setInterval(() => {
      this.nextFeed();
    }, 15000);
  }

  nextFeed() {
    this.currentFeedIndex = (this.currentFeedIndex + 1) % this.feeds.length;
    this.switchFeed();
  }

  previousFeed() {
    this.currentFeedIndex = (this.currentFeedIndex - 1 + this.feeds.length) % this.feeds.length;
    this.switchFeed();
  }

  switchFeed() {
    const currentFeed = this.feeds[this.currentFeedIndex];
    
    // Update UI
    document.getElementById('feedTitle').textContent = currentFeed.name;
    document.getElementById('feedLocation').textContent = currentFeed.location;
    
    // Dispatch event
    window.dispatchEvent(new CustomEvent('feedChanged', {
      detail: { 
        name: currentFeed.name,
        location: currentFeed.location,
        index: this.currentFeedIndex
      }
    }));
    
    // In a real implementation, this would switch video sources
    this.statusElement.textContent = `Switched to ${currentFeed.name}`;
  }

  captureScreenshot() {
    const canvas = document.createElement('canvas');
    const videoContainer = document.getElementById('videoContainer');
    
    canvas.width = videoContainer.clientWidth;
    canvas.height = videoContainer.clientHeight;
    
    const ctx = canvas.getContext('2d');
    
    // Capture the video or placeholder
    if (this.videoElement.readyState >= HTMLMediaElement.HAVE_CURRENT_DATA) {
      ctx.drawImage(this.videoElement, 0, 0, canvas.width, canvas.height);
    } else {
      // Capture the placeholder canvas
      const placeholderCanvas = document.getElementById('placeholderCanvas');
      if (placeholderCanvas) {
        ctx.drawImage(placeholderCanvas, 0, 0);
      }
    }
    
    // Add timestamp overlay
    ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
    ctx.fillRect(10, canvas.height - 40, 200, 30);
    ctx.fillStyle = '#00ffe0';
    ctx.font = '14px monospace';
    ctx.fillText(new Date().toLocaleString(), 20, canvas.height - 18);
    
    // Create download
    const dataUrl = canvas.toDataURL('image/png');
    const link = document.createElement('a');
    link.download = `federal-way-feed-${Date.now()}.png`;
    link.href = dataUrl;
    link.click();
    
    // Dispatch event for external handling (e.g., Google Drive upload)
    window.dispatchEvent(new CustomEvent('screenshotCaptured', {
      detail: { 
        dataUrl,
        timestamp: new Date().toISOString(),
        feedName: this.feeds[this.currentFeedIndex].name
      }
    }));
    
    // Visual feedback
    this.showCaptureFlash();
  }

  showCaptureFlash() {
    const flash = document.createElement('div');
    flash.style.position = 'absolute';
    flash.style.top = '0';
    flash.style.left = '0';
    flash.style.width = '100%';
    flash.style.height = '100%';
    flash.style.backgroundColor = 'white';
    flash.style.opacity = '0.8';
    flash.style.zIndex = '1000';
    flash.style.pointerEvents = 'none';
    
    const videoContainer = document.getElementById('videoContainer');
    videoContainer.appendChild(flash);
    
    setTimeout(() => {
      flash.style.transition = 'opacity 0.3s';
      flash.style.opacity = '0';
      setTimeout(() => flash.remove(), 300);
    }, 100);
  }

  // Method to integrate actual video stream (when available)
  async connectToStream(streamUrl) {
    try {
      this.statusElement.textContent = 'Connecting to live feed...';
      
      // For actual implementation with video streams
      // This would use HLS.js, WebRTC, or similar
      if (this.videoElement) {
        this.videoElement.src = streamUrl;
        await this.videoElement.play();
        this.isStreaming = true;
        this.statusElement.textContent = 'Connected';
        
        // Hide overlay after connection
        setTimeout(() => {
          const overlay = document.getElementById('videoOverlay');
          overlay.style.opacity = '0';
          setTimeout(() => overlay.style.display = 'none', 500);
        }, 1000);
      }
      
      this.reconnectAttempts = 0;
    } catch (error) {
      console.error('Failed to connect to stream:', error);
      this.handleStreamError(error);
    }
  }

  handleStreamError(error) {
    this.isStreaming = false;
    this.reconnectAttempts++;
    
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.statusElement.textContent = `Connection error. Retrying (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`;
      setTimeout(() => this.reconnect(), 3000);
    } else {
      this.statusElement.textContent = 'Stream unavailable. Using placeholder mode.';
    }
  }

  reconnect() {
    const currentFeed = this.feeds[this.currentFeedIndex];
    this.connectToStream(currentFeed.url);
  }

  destroy() {
    if (this.videoElement) {
      this.videoElement.pause();
      this.videoElement.src = '';
    }
    this.isStreaming = false;
  }

  // Public methods
  getCurrentFeed() {
    return this.feeds[this.currentFeedIndex];
  }

  getFeedCount() {
    return this.feeds.length;
  }

  setFeed(index) {
    if (index >= 0 && index < this.feeds.length) {
      this.currentFeedIndex = index;
      this.switchFeed();
    }
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = FederalWayLiveFeed;
}
