# 🎨 IDS Detection - Frontend Dashboard

Modern, real-time web dashboard for the Multi-Stage Intrusion Detection System.

## ✨ Features

### 📊 Real-Time Detection Feed
- Live attack detection notifications
- Color-coded severity indicators (Critical/High/Medium/Low)
- Confidence score visualization
- Source/Destination IP tracking
- Port and protocol information

### 🚨 Critical Alert System
- Pop-up notifications for high-confidence threats (>90%)
- Auto-dismissing alerts with manual override
- Sound/visual notifications
- Alert history tracking (prevents duplicate alerts)

### 🔍 Threat Intelligence Page
- Dedicated view for attack history
- Stores up to 1,000 critical threats
- Filterable and sortable threat table
- Detailed attack information per entry
- Export functionality (future enhancement)

### 📈 System Metrics
- Total packets processed
- Attacks detected count
- System health percentage
- Real-time status indicators

### 🎯 User Experience
- Responsive design (mobile, tablet, desktop)
- Smooth animations and transitions
- Lucide React icons for consistency
- Dark mode optimized color scheme
- Intuitive navigation

---

## 🛠️ Tech Stack

- **React 19.2.0**: Modern hooks-based architecture
- **Vite 7.2.4**: Lightning-fast dev server and builds
- **Lucide React 0.562**: Beautiful icon library
- **ESLint**: Code quality and consistency
- **CSS3**: Custom styling with CSS variables

---

## 🚀 Getting Started

### Prerequisites
```bash
Node.js 16+
npm or yarn
```

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Environment Variables

The frontend connects to the backend API at:
```javascript
const API_BASE = 'http://127.0.0.1:8000';
```

To change the API endpoint, modify `API_BASE` in [src/App.jsx](src/App.jsx).

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── App.jsx          # Main dashboard component
│   ├── Threats.jsx      # Threat intelligence page
│   ├── App.css          # Global styles
│   ├── index.css        # Base styles
│   └── main.jsx         # React entry point
│
├── public/              # Static assets
├── index.html           # HTML template
├── vite.config.js       # Vite configuration
├── package.json         # Dependencies
└── README.md
```

---

## 🎨 Components

### App.jsx
Main dashboard with:
- Real-time detection feed
- System metrics panel
- Critical alert notifications
- Navigation between pages

### Threats.jsx
Threat intelligence page with:
- Attack history table
- Severity filtering
- Detailed threat information
- Export capabilities

---

## 🔧 Development

### Available Scripts

```bash
# Development mode with hot reload
npm run dev

# Build for production
npm run build

# Lint code
npm run lint

# Preview production build
npm run preview
```

### Code Style

This project uses ESLint with React-specific rules:
- React Hooks rules enforced
- React Refresh plugin for HMR
- ES6+ modern JavaScript

---

## 🎯 API Integration

The dashboard connects to these backend endpoints:

```javascript
GET  /detections     # Fetch recent detections
GET  /threats        # Fetch threat history
GET  /model-info     # Get model metadata
GET  /               # Health check
```

All endpoints are polled every 2 seconds for real-time updates.

---

## 🌈 Customization

### Changing Colors

Edit CSS variables in `src/App.css`:
```css
:root {
  --primary-color: #your-color;
  --danger-color: #your-color;
  --success-color: #your-color;
}
```

### Adjusting Update Frequency

Modify the polling interval in `src/App.jsx`:
```javascript
const interval = setInterval(fetchDetections, 2000); // 2 seconds
```

---

## 📱 Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

---

## 🤝 Contributing

When contributing to the frontend:
1. Follow existing component structure
2. Use functional components with hooks
3. Maintain responsive design principles
4. Test on multiple browsers
5. Update this README if adding features

---

## 📄 License

MIT License - see main project LICENSE

---

<div align="center">

**Part of the Multi-Stage IDS Detection System**

[Main Documentation](../README.md) | [Backend](../backend/) | [Setup Guide](../SETUP.md)

</div>
