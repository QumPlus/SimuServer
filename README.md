# SimuServer - Universal API Simulation Tool

![SimuServer Logo](https://img.shields.io/badge/SimuServer-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Created by QumPlus**

SimuServer is a lightweight, powerful, and user-friendly server simulation tool designed for developers, testers, and anyone who needs to simulate popular APIs for testing applications locally. Whether you're building the next Instagram, developing a messaging app, or creating an e-commerce platform, SimuServer provides realistic API endpoints to help you develop and test your applications.

## 🚀 Features

### ✨ Core Capabilities
- **Lightweight HTTP/REST Server** - Built with FastAPI for high performance
- **Real-time WebSocket Support** - Perfect for messaging and live applications
- **Pre-built API Templates** - Instagram, Messenger, Twitter, E-commerce, and Authentication APIs
- **Custom Data Directory** - Choose where your server data is stored
- **Real-time Performance Monitoring** - CPU, RAM, Network, and request analytics
- **Modern GUI** - Beautiful dark-themed interface with customtkinter
- **Request Inspector** - Postman-like request/response analysis

### 🛠 Advanced Features
- **Error Simulation** - Inject artificial delays and errors for robust testing
- **Authentication Emulation** - JWT and cookie-based session simulation
- **Custom Template Loading** - Load your own JSON-based API templates
- **Real-time Logging** - Comprehensive logging with filtering and export
- **Performance Analytics** - Detailed metrics and request tracking
- **Cross-platform** - Works on Windows, macOS, and Linux

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)

### Quick Start
1. **Clone the repository**
   ```bash
   git clone https://github.com/QumPlus/SimuServer.git
   cd SimuServer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run SimuServer**
   ```bash
   python main.py
   ```

That's it! SimuServer will launch with a modern GUI interface.

## 🎯 Usage Guide

### Starting Your First Simulation

1. **Launch SimuServer** and you'll see the main dashboard
2. **Navigate to the "API Simulator" tab**
3. **Select a template** from the dropdown (e.g., "Instagram API")
4. **Click "Load Template"** to activate the API endpoints
5. **Click "Start Server"** in the header
6. **Your API is now running!** Visit `http://localhost:8000` to see it in action

### Available API Templates

#### 📱 Instagram API
Perfect for social media applications:
- `GET /api/instagram/users/me` - User profile
- `GET /api/instagram/posts` - Posts feed
- `POST /api/instagram/posts` - Create new post
- `POST /api/instagram/posts/{id}/like` - Like a post

#### 💬 Messenger API
Great for messaging applications:
- `GET /api/messenger/conversations` - List conversations
- `GET /api/messenger/conversations/{id}/messages` - Get messages
- `POST /api/messenger/conversations/{id}/messages` - Send message

#### 🐦 Twitter API
Ideal for microblogging platforms:
- `GET /api/twitter/timeline` - Get timeline
- `POST /api/twitter/tweets` - Create tweet
- `POST /api/twitter/tweets/{id}/like` - Like tweet

#### 🛒 E-commerce API
Perfect for online stores:
- `GET /api/ecommerce/products` - List products
- `GET /api/ecommerce/cart` - Get shopping cart
- `POST /api/ecommerce/cart/add` - Add to cart
- `POST /api/ecommerce/checkout` - Process checkout

#### 🔐 Authentication API
Essential for user management:
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/logout` - User logout

### WebSocket Support

SimuServer includes WebSocket endpoints for real-time features:
- `ws://localhost:8000/ws` - General WebSocket endpoint
- `ws://localhost:8000/ws/chat` - Chat-specific WebSocket

Example JavaScript connection:
```javascript
const socket = new WebSocket('ws://localhost:8000/ws/chat');
socket.onopen = () => {
    socket.send(JSON.stringify({
        user: "TestUser",
        message: "Hello World!"
    }));
};
```

## 🎨 GUI Features

### 📊 Performance Tab
Monitor your simulation in real-time:
- **CPU Usage** - Real-time CPU monitoring with visual indicators
- **Memory Usage** - RAM consumption tracking
- **Request Metrics** - Requests per second, total requests, response times
- **Network Statistics** - Data transfer monitoring
- **System Information** - Core count, disk usage, uptime

### 🔍 Request Inspector
Analyze your API calls like a pro:
- **Request List** - See all incoming requests in real-time
- **Detailed Analysis** - View headers, body, and response data
- **Filtering** - Filter by method, status code, or search terms
- **Export** - Export request data to JSON for analysis

### 📝 Logs Tab
Complete logging solution:
- **Real-time Logs** - See all server activity instantly
- **Search & Filter** - Find specific log entries quickly
- **Export Logs** - Save logs to files for later analysis
- **Auto-scroll** - Automatically follow new log entries

### 💾 Storage Tab
Manage your data directory:
- **Directory Management** - Choose where your data is stored
- **File Browser** - See what files are created by your simulations
- **Cleanup Tools** - Remove temporary files and manage storage
- **Backup** - Create backups of your simulation data

## ⚙️ Configuration

SimuServer creates a `simuserver_config.json` file for configuration:

```json
{
  "server": {
    "host": "127.0.0.1",
    "port": 8000,
    "auto_start": false,
    "enable_websockets": true
  },
  "storage": {
    "data_directory": "/path/to/your/data",
    "auto_create": true,
    "max_file_size_mb": 100
  },
  "simulation": {
    "default_delay_ms": 0,
    "error_rate": 0.0,
    "enable_cors": true
  }
}
```

### Simulation Settings
- **Response Delay** - Add artificial delay to responses (in milliseconds)
- **Error Rate** - Inject random errors (0.0 = no errors, 1.0 = all errors)
- **CORS** - Enable/disable Cross-Origin Resource Sharing

## 🔧 Creating Custom Templates

Create your own API templates with JSON files:

```json
{
  "name": "My Custom API",
  "description": "A custom API for my application",
  "version": "1.0",
  "routes": [
    {
      "method": "GET",
      "path": "/api/custom/data",
      "response": {
        "message": "Hello from custom API!",
        "data": [1, 2, 3, 4, 5]
      },
      "status_code": 200
    }
  ]
}
```

Load custom templates via the "Load Custom" button in the API Simulator tab.

## 🚀 Use Cases

### 🏗️ Application Development
- **Frontend Development** - Build UIs without waiting for backend APIs
- **Mobile Apps** - Test iOS/Android apps with realistic API responses
- **Web Applications** - Develop React, Vue, or Angular apps with mock data

### 🧪 Testing & QA
- **Integration Testing** - Test how your app handles various API responses
- **Error Handling** - Simulate server errors and network issues
- **Performance Testing** - Test app behavior under different response times

### 📚 Learning & Prototyping
- **API Design** - Prototype API structures before implementation
- **Learning** - Understand how popular APIs work
- **Demos** - Create impressive demos with realistic data

### 👥 Team Collaboration
- **Parallel Development** - Frontend and backend teams work simultaneously
- **Client Demos** - Show clients working prototypes without full backend
- **Workshops** - Teach API concepts with hands-on examples

## 🤝 Contributing

I welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Areas for Contribution
- **New API Templates** - Add templates for popular services
- **GUI Improvements** - Enhance the user interface
- **Performance Optimizations** - Make SimuServer even faster
- **Documentation** - Improve guides and examples
- **Testing** - Add unit tests and integration tests

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** - For the amazing web framework
- **CustomTkinter** - For the beautiful modern GUI components
- **psutil** - For system monitoring capabilities
- **uvicorn** - For the high-performance ASGI server

## 📞 Support & Contact

- **Issues** - Report bugs and request features on [GitHub Issues](https://github.com/QumPlus/SimuServer/issues)
- **Creator** - QumPlus
- **Version** - 1.0.0

---

**Made with ❤️ by QumPlus**

*SimuServer - Making API simulation simple, powerful, and beautiful.* 
