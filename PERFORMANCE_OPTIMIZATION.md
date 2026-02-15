# Performance Optimization Guide

## Overview
This document outlines the performance improvements made to the CEC-WAM-HOT-CORE codebase and best practices for maintaining optimal performance.

## Recent Optimizations

### 1. Streamlit Dashboard (app.py)

#### Critical Fixes
- **Removed Infinite Rerun Loop**: Eliminated `st.rerun()` in TAB 6 which was causing continuous page refreshes every 2 seconds
  - Impact: Drastically reduced CPU usage and improved user experience
  - Solution: Replaced with informational message about manual refresh

#### Data Caching
- **Seeded Random Data**: Implemented hour-based seeding for random data generation
  - Charts and metrics now update every hour instead of every render
  - Prevents flickering and reduces computation overhead
  - Areas affected: TAB 6 metrics, price history charts, neural network visualization

#### Best Practices
```python
# Cache random data with time-based seed
random.seed(st.session_state.cached_random_seed)
data = [generate_random_value() for _ in range(n)]
random.seed()  # Reset to unpredictable state
```

### 2. EVE Voice Agent (eve_voice_agent.py)

#### Memory Management
- **Bounded Collections**: Replaced unbounded lists with `collections.deque`
  - Conversation history: `deque(maxlen=100)` - stores 50 exchanges
  - Logs: `deque(maxlen=1000)` - auto-trims old entries
  - Impact: Prevents memory bloat in long-running sessions

#### Computation Optimization
- **Cached System Prompt**: System prompt is now built once and cached
  - Previously rebuilt on every chat interaction
  - Reduces string concatenation overhead

#### Security & Performance
- **AST-based Math Evaluation**: Replaced `eval()` with safer AST parsing
  - More secure than eval() with restricted builtins
  - Better performance for mathematical expressions
  - Supports: +, -, *, /, pow, abs, round, min, max, sum

#### Best Practices
```python
from collections import deque

# Use bounded deque for auto-trimming collections
history = deque(maxlen=100)

# Cache expensive operations
if self._cached_value is None:
    self._cached_value = expensive_operation()
return self._cached_value
```

### 3. HTML Dashboard (index.html)

#### Rendering Optimization
- **Cached Star Field**: 10,000 star vertices generated once and cached
  - Previously regenerated on every unlock
  - Impact: Faster initialization, reduced memory allocation

#### Network Optimization
- **Parallel API Calls**: Using `Promise.all()` for concurrent fetching
  - PSI price and Google Sheets data load simultaneously
  - Faster initial page load

#### Event Handling
- **Debounced Resize Handler**: Window resize events throttled to 250ms
  - Prevents excessive camera/renderer updates
  - Reduces CPU usage during window resizing

#### Smart Refresh
- **Visibility-based Updates**: Auto-refresh only when page is visible
  - Uses Page Visibility API to detect tab state
  - Saves bandwidth and reduces unnecessary API calls

#### Best Practices
```javascript
// Cache expensive computations
let cachedData = null;
function getData() {
    if (!cachedData) {
        cachedData = expensiveComputation();
    }
    return cachedData;
}

// Debounce frequent events
let timeout;
window.addEventListener('resize', () => {
    clearTimeout(timeout);
    timeout = setTimeout(handleResize, 250);
});

// Parallel async operations
Promise.all([fetch1(), fetch2(), fetch3()])
    .then(results => processResults(results));
```

## Performance Monitoring

### Key Metrics to Watch
1. **Memory Usage**: Monitor for memory leaks in long-running sessions
2. **API Call Frequency**: Ensure auto-refresh intervals are appropriate
3. **Render Time**: Check browser dev tools for slow render operations
4. **Network Bandwidth**: Monitor data transfer sizes

### Recommended Tools
- Chrome DevTools Performance tab
- Streamlit's built-in profiling
- Network tab for API call monitoring

## Configuration Tuning

### Streamlit Cache Settings
```python
# Adjust cache TTL based on data volatility
@st.cache_data(ttl=3600)  # 1 hour for stable data
def fetch_stable_data():
    pass

@st.cache_data(ttl=60)  # 1 minute for frequently changing data
def fetch_live_data():
    pass
```

### API Rate Limits
- NASA APOD: Cache for 3600s (1 hour)
- Google Sheets: Cache for 60s (1 minute)
- CoinGecko: Consider implementing exponential backoff

## Future Optimization Opportunities

### High Priority
1. Implement incremental chart updates instead of full recreation
2. Add server-side caching layer for API responses
3. Optimize CSS animations (disable on low-power devices)
4. Implement lazy loading for off-screen content

### Medium Priority
1. Use WebAssembly for intensive calculations
2. Implement service worker for offline functionality
3. Add image lazy loading and compression
4. Optimize Three.js rendering with LOD (Level of Detail)

### Low Priority
1. Add dark/light theme toggle
2. Implement progressive web app (PWA) features
3. Add performance budgets to CI/CD pipeline

## Troubleshooting

### High CPU Usage
- Check for infinite loops or excessive reruns
- Verify auto-refresh intervals are reasonable
- Disable unnecessary animations

### Memory Leaks
- Ensure all collections use bounded storage
- Check for event listener cleanup
- Monitor long-running sessions

### Slow Page Load
- Review API call sequence (should be parallel)
- Check for blocking JavaScript operations
- Verify caching is properly configured

### UI Flickering
- Ensure random data uses consistent seeds
- Check for unnecessary component re-renders
- Verify chart updates are incremental

## Best Practices Summary

1. **Cache Aggressively**: Cache API responses, computed values, and expensive operations
2. **Bound Collections**: Use `deque` or similar for collections that grow over time
3. **Debounce Events**: Throttle frequent events like resize, scroll, input
4. **Parallel Operations**: Use `Promise.all()` or async/await for concurrent tasks
5. **Lazy Loading**: Load resources only when needed
6. **Monitor Performance**: Regularly profile and optimize bottlenecks
7. **Document Changes**: Keep this guide updated with new optimizations

## Contact

For questions or suggestions about performance optimization, please open an issue in the repository.
