"""
Server engine for SimuServer - FastAPI-based HTTP and WebSocket server
"""

import asyncio
import threading
import time
import uvicorn
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path

from fastapi import FastAPI, Request, Response, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import psutil

from .request_logger import RequestLogger
from .performance_monitor import PerformanceMonitor

class ServerEngine:
    """Main server engine using FastAPI"""
    
    def __init__(self, config, log_callback: Optional[Callable] = None):
        self.config = config
        self.log_callback = log_callback
        self.app = FastAPI(title="SimuServer", description="Universal API Simulation Tool")
        self.server = None
        self.server_thread = None
        self.is_running = False
        self.start_time = None
        
        # Components
        self.request_logger = RequestLogger(max_entries=config.get("logging.max_entries", 1000))
        self.performance_monitor = PerformanceMonitor(
            update_interval=config.get("performance.update_interval", 1.0)
        )
        
        # WebSocket connections
        self.websocket_connections: List[WebSocket] = []
        
        # Templates and routes
        self.active_templates: List[str] = []
        self.custom_routes: Dict[str, Any] = {}
        
        self._setup_middleware()
        self._setup_default_routes()
        self._setup_websocket_routes()
    
    def _setup_middleware(self):
        """Setup FastAPI middleware"""
        # CORS middleware
        if self.config.get("simulation.enable_cors", True):
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        
        # Request logging middleware
        @self.app.middleware("http")
        async def log_requests(request: Request, call_next):
            start_time = time.time()
            
            # Add artificial delay if configured
            delay = self.config.get("simulation.default_delay_ms", 0)
            if delay > 0:
                await asyncio.sleep(delay / 1000)
            
            # Simulate errors if configured
            error_rate = self.config.get("simulation.error_rate", 0.0)
            if error_rate > 0 and time.time() % 1 < error_rate:
                return JSONResponse(
                    status_code=500,
                    content={"error": "Simulated server error"}
                )
            
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log the request
            self.request_logger.log_request(
                method=request.method,
                url=str(request.url),
                headers=dict(request.headers),
                status_code=response.status_code,
                response_time=process_time,
                timestamp=datetime.now()
            )
            
            # Update performance metrics
            self.performance_monitor.update_request_count()
            
            # Notify GUI if callback provided
            if self.log_callback:
                self.log_callback(f"{request.method} {request.url.path} - {response.status_code} ({process_time:.3f}s)")
            
            return response
    
    def _setup_default_routes(self):
        """Setup default API routes"""
        
        @self.app.get("/")
        async def root():
            return {
                "message": "SimuServer is running!",
                "version": "1.0.0",
                "uptime": time.time() - self.start_time if self.start_time else 0,
                "active_templates": self.active_templates
            }
        
        @self.app.get("/health")
        async def health_check():
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "uptime": time.time() - self.start_time if self.start_time else 0
            }
        
        @self.app.get("/api/status")
        async def server_status():
            """Get server status and metrics"""
            metrics = self.performance_monitor.get_current_metrics()
            return {
                "status": "running",
                "uptime": time.time() - self.start_time if self.start_time else 0,
                "performance": metrics,
                "active_templates": self.active_templates,
                "total_requests": self.request_logger.get_total_requests(),
                "connected_websockets": len(self.websocket_connections)
            }
        
        @self.app.get("/api/requests")
        async def get_requests():
            """Get recent requests for inspection"""
            return self.request_logger.get_recent_requests()
        
        @self.app.post("/api/simulate/error")
        async def simulate_error(error_code: int = 500):
            """Simulate specific HTTP error"""
            raise HTTPException(status_code=error_code, detail=f"Simulated {error_code} error")
    
    def _setup_websocket_routes(self):
        """Setup WebSocket routes"""
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            self.websocket_connections.append(websocket)
            
            try:
                while True:
                    data = await websocket.receive_text()
                    # Echo the message back to all connected clients
                    await self._broadcast_message(f"Echo: {data}")
            except Exception as e:
                if self.log_callback:
                    self.log_callback(f"WebSocket disconnected: {str(e)}")
            finally:
                if websocket in self.websocket_connections:
                    self.websocket_connections.remove(websocket)
        
        @self.app.websocket("/ws/chat")
        async def chat_websocket(websocket: WebSocket):
            """Simple chat WebSocket for testing messaging apps"""
            await websocket.accept()
            self.websocket_connections.append(websocket)
            
            try:
                while True:
                    data = await websocket.receive_json()
                    message = {
                        "id": int(time.time() * 1000),
                        "user": data.get("user", "Anonymous"),
                        "message": data.get("message", ""),
                        "timestamp": datetime.now().isoformat()
                    }
                    await self._broadcast_message(message)
            except Exception:
                pass
            finally:
                if websocket in self.websocket_connections:
                    self.websocket_connections.remove(websocket)
    
    async def _broadcast_message(self, message: Any):
        """Broadcast message to all connected WebSocket clients"""
        if not self.websocket_connections:
            return
        
        disconnected = []
        for websocket in self.websocket_connections:
            try:
                if isinstance(message, str):
                    await websocket.send_text(message)
                else:
                    await websocket.send_json(message)
            except Exception:
                disconnected.append(websocket)
        
        # Remove disconnected clients
        for ws in disconnected:
            if ws in self.websocket_connections:
                self.websocket_connections.remove(ws)
    
    def load_template(self, template_name: str, template_data: Dict[str, Any]):
        """Load an API template"""
        try:
            routes = template_data.get("routes", [])
            for route in routes:
                self._add_dynamic_route(
                    method=route["method"],
                    path=route["path"],
                    response=route["response"],
                    status_code=route.get("status_code", 200)
                )
            
            self.active_templates.append(template_name)
            if self.log_callback:
                self.log_callback(f"Loaded template: {template_name}")
            
        except Exception as e:
            if self.log_callback:
                self.log_callback(f"Error loading template {template_name}: {str(e)}")
    
    def _add_dynamic_route(self, method: str, path: str, response: Any, status_code: int = 200):
        """Add a dynamic route to the FastAPI app"""
        async def dynamic_handler(request: Request):
            return JSONResponse(content=response, status_code=status_code)
        
        # Add route based on method
        if method.upper() == "GET":
            self.app.get(path)(dynamic_handler)
        elif method.upper() == "POST":
            self.app.post(path)(dynamic_handler)
        elif method.upper() == "PUT":
            self.app.put(path)(dynamic_handler)
        elif method.upper() == "DELETE":
            self.app.delete(path)(dynamic_handler)
    
    def start_server(self):
        """Start the server in a separate thread"""
        if self.is_running:
            return False
        
        def run_server():
            self.start_time = time.time()
            self.performance_monitor.start()
            
            config = uvicorn.Config(
                self.app,
                host=self.config.get("server.host", "127.0.0.1"),
                port=self.config.get("server.port", 8000),
                log_level="info"
            )
            self.server = uvicorn.Server(config)
            asyncio.run(self.server.serve())
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        self.is_running = True
        
        if self.log_callback:
            self.log_callback(f"Server started on {self.config.get('server.host')}:{self.config.get('server.port')}")
        
        return True
    
    def stop_server(self):
        """Stop the server"""
        if not self.is_running or not self.server:
            return False
        
        self.server.should_exit = True
        self.performance_monitor.stop()
        self.is_running = False
        
        if self.log_callback:
            self.log_callback("Server stopped")
        
        return True
    
    def get_performance_data(self):
        """Get current performance metrics"""
        return self.performance_monitor.get_current_metrics()
    
    def get_request_history(self):
        """Get request history for inspection"""
        return self.request_logger.get_recent_requests() 