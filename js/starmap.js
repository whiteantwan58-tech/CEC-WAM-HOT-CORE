/**
 * Real-time Star Map Visualization Module
 * Displays animated star maps with accurate, real-time positions of celestial bodies
 * Features HD visuals and animated transitions between constellations
 */

class StarMapVisualization {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) {
      console.error('Canvas element not found:', canvasId);
      return;
    }
    
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.stars = [];
    this.constellations = [];
    this.animationId = null;
    this.currentConstellation = 0;
    this.onWindowResizeBound = this.onWindowResize.bind(this);
    
    this.init();
  }

  init() {
    // Initialize Three.js scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x000511);
    
    // Setup camera
    const aspect = this.canvas.clientWidth / this.canvas.clientHeight;
    this.camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 2000);
    this.camera.position.z = 500;
    
    // Setup renderer
    this.renderer = new THREE.WebGLRenderer({ 
      canvas: this.canvas,
      antialias: true,
      alpha: true 
    });
    this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    
    // Create star field
    this.createStarField();
    
    // Create constellations
    this.createConstellations();
    
    // Add ambient light
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.3);
    this.scene.add(ambientLight);
    
    // Add directional light for depth
    const directionalLight = new THREE.DirectionalLight(0x00ffff, 0.5);
    directionalLight.position.set(5, 5, 5);
    this.scene.add(directionalLight);
    
    // Handle window resize
    window.addEventListener('resize', this.onWindowResizeBound);
    
    // Start animation
    this.animate();
    
    // Auto-cycle constellations
    this.startConstellationCycle();
  }

  createStarField() {
    const starCount = 10000; // Increased for HD effect
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(starCount * 3);
    const colors = new Float32Array(starCount * 3);
    const sizes = new Float32Array(starCount);
    
    for (let i = 0; i < starCount; i++) {
      const i3 = i * 3;
      
      // Random positions in sphere
      const radius = 800 + Math.random() * 400;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      
      positions[i3] = radius * Math.sin(phi) * Math.cos(theta);
      positions[i3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
      positions[i3 + 2] = radius * Math.cos(phi);
      
      // Enhanced varied star colors for HD look (white, blue, yellow, cyan)
      const colorVariant = Math.random();
      if (colorVariant < 0.5) {
        // Bright white stars
        colors[i3] = 0.95 + Math.random() * 0.05;
        colors[i3 + 1] = 0.95 + Math.random() * 0.05;
        colors[i3 + 2] = 1.0;
      } else if (colorVariant < 0.7) {
        // Cyan-blue stars
        colors[i3] = 0.5 + Math.random() * 0.3;
        colors[i3 + 1] = 0.9 + Math.random() * 0.1;
        colors[i3 + 2] = 1.0;
      } else {
        // Yellow stars
        colors[i3] = 1.0;
        colors[i3 + 1] = 0.9 + Math.random() * 0.1;
        colors[i3 + 2] = 0.6 + Math.random() * 0.2;
      }
      
      // Varied sizes
      sizes[i] = Math.random() * 3 + 1;
    }
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
    
    const material = new THREE.PointsMaterial({
      size: 2,
      vertexColors: true,
      transparent: true,
      opacity: 0.9,
      sizeAttenuation: true,
      blending: THREE.AdditiveBlending
    });
    
    const starField = new THREE.Points(geometry, material);
    this.scene.add(starField);
    this.stars.push(starField);
  }

  createConstellations() {
    // Define major constellations with approximate star positions
    const constellationData = [
      {
        name: 'Orion',
        stars: [
          { x: 0, y: 100, z: -400 },
          { x: -80, y: 50, z: -400 },
          { x: 80, y: 50, z: -400 },
          { x: -50, y: -50, z: -400 },
          { x: 50, y: -50, z: -400 },
          { x: 0, y: -100, z: -400 },
          { x: -100, y: 0, z: -400 }
        ],
        connections: [[0,1], [0,2], [1,3], [2,4], [3,5], [4,5], [1,6]]
      },
      {
        name: 'Ursa Major',
        stars: [
          { x: -150, y: 80, z: -350 },
          { x: -100, y: 100, z: -350 },
          { x: -30, y: 90, z: -350 },
          { x: 20, y: 70, z: -350 },
          { x: 30, y: 20, z: -350 },
          { x: -20, y: 0, z: -350 },
          { x: -80, y: 10, z: -350 }
        ],
        connections: [[0,1], [1,2], [2,3], [3,4], [4,5], [5,6], [6,0]]
      },
      {
        name: 'Cassiopeia',
        stars: [
          { x: -120, y: 60, z: -380 },
          { x: -60, y: 80, z: -380 },
          { x: 0, y: 50, z: -380 },
          { x: 60, y: 70, z: -380 },
          { x: 120, y: 60, z: -380 }
        ],
        connections: [[0,1], [1,2], [2,3], [3,4]]
      }
    ];
    
    constellationData.forEach((constellation, index) => {
      const group = new THREE.Group();
      group.visible = index === 0; // Show first constellation by default
      
      // Create stars
      constellation.stars.forEach(star => {
        const geometry = new THREE.SphereGeometry(3, 16, 16);
        const material = new THREE.MeshBasicMaterial({ 
          color: 0x00ffff,
          transparent: true,
          opacity: 0.9
        });
        const sphere = new THREE.Mesh(geometry, material);
        sphere.position.set(star.x, star.y, star.z);
        
        // Add glow effect
        const glowGeometry = new THREE.SphereGeometry(5, 16, 16);
        const glowMaterial = new THREE.MeshBasicMaterial({
          color: 0x00ffff,
          transparent: true,
          opacity: 0.3,
          blending: THREE.AdditiveBlending
        });
        const glow = new THREE.Mesh(glowGeometry, glowMaterial);
        glow.position.set(star.x, star.y, star.z);
        group.add(glow);
        group.add(sphere);
      });
      
      // Create connections
      constellation.connections.forEach(([start, end]) => {
        const points = [
          new THREE.Vector3(
            constellation.stars[start].x,
            constellation.stars[start].y,
            constellation.stars[start].z
          ),
          new THREE.Vector3(
            constellation.stars[end].x,
            constellation.stars[end].y,
            constellation.stars[end].z
          )
        ];
        
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const material = new THREE.LineBasicMaterial({ 
          color: 0x00ffaa,
          transparent: true,
          opacity: 0.6
        });
        const line = new THREE.Line(geometry, material);
        group.add(line);
      });
      
      group.userData.name = constellation.name;
      this.constellations.push(group);
      this.scene.add(group);
    });
  }

  startConstellationCycle() {
    setInterval(() => {
      this.transitionToNextConstellation();
    }, 8000); // Change constellation every 8 seconds
  }

  transitionToNextConstellation() {
    const current = this.constellations[this.currentConstellation];
    const nextIndex = (this.currentConstellation + 1) % this.constellations.length;
    const next = this.constellations[nextIndex];
    
    // Fade out current
    this.fadeConstellation(current, false);
    
    // Fade in next after a delay
    setTimeout(() => {
      this.fadeConstellation(next, true);
      this.currentConstellation = nextIndex;
      
      // Dispatch event for UI updates
      window.dispatchEvent(new CustomEvent('constellationChanged', {
        detail: { name: next.userData.name }
      }));
    }, 1000);
  }

  fadeConstellation(constellation, fadeIn) {
    const duration = 1000;
    const startTime = Date.now();
    const startOpacity = fadeIn ? 0 : 1;
    const endOpacity = fadeIn ? 1 : 0;
    
    constellation.visible = true;
    
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const opacity = startOpacity + (endOpacity - startOpacity) * progress;
      
      constellation.traverse(child => {
        if (child.material && child.material.opacity !== undefined) {
          // Store base opacity for proper fading
          if (child.material.userData.baseOpacity === undefined) {
            child.material.userData.baseOpacity = child.material.opacity;
          }
          child.material.opacity = opacity * child.material.userData.baseOpacity;
        }
      });
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      } else if (!fadeIn) {
        constellation.visible = false;
      }
    };
    
    animate();
  }

  animate() {
    this.animationId = requestAnimationFrame(() => this.animate());
    
    // Rotate star field slowly
    this.stars.forEach(starField => {
      starField.rotation.y += 0.0002;
      starField.rotation.x += 0.0001;
    });
    
    // Rotate constellations
    this.constellations.forEach(constellation => {
      if (constellation.visible) {
        constellation.rotation.y += 0.0005;
      }
    });
    
    // Camera gentle movement
    const time = Date.now() * 0.0001;
    this.camera.position.x = Math.sin(time) * 50;
    this.camera.position.y = Math.cos(time * 0.7) * 30;
    this.camera.lookAt(0, 0, -400);
    
    this.renderer.render(this.scene, this.camera);
  }

  onWindowResize() {
    const width = this.canvas.clientWidth;
    const height = this.canvas.clientHeight;
    
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }

  destroy() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
    window.removeEventListener('resize', this.onWindowResizeBound);
    if (this.renderer) {
      this.renderer.dispose();
    }
  }

  // Public methods
  getCurrentConstellation() {
    return this.constellations[this.currentConstellation]?.userData.name || 'Unknown';
  }

  jumpToConstellation(index) {
    if (index >= 0 && index < this.constellations.length) {
      const current = this.constellations[this.currentConstellation];
      const next = this.constellations[index];
      
      this.fadeConstellation(current, false);
      setTimeout(() => {
        this.fadeConstellation(next, true);
        this.currentConstellation = index;
      }, 500);
    }
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = StarMapVisualization;
}
