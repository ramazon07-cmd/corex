"""
CoreX Agent - CLI↔GUI Synchronization Server
"""

import os
import sys
import json
import asyncio
import websockets
import subprocess
import threading
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import secrets


class CoreXAgent:
    """WebSocket server for CLI↔GUI synchronization"""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Dict[str, Any] = {}
        self.processes: Dict[str, subprocess.Popen] = {}
        self.tokens: Dict[str, str] = {}
        
    async def register_client(self, websocket: Any, token: str) -> Optional[str]:
        """Register a new client with authentication token"""
        if token not in self.tokens.values():
            await websocket.close(1008, "Invalid authentication token")
            return None
            
        client_id = secrets.token_urlsafe(16)
        self.clients[client_id] = websocket
        return client_id
    
    async def unregister_client(self, client_id: str):
        """Unregister a client"""
        if client_id in self.clients:
            del self.clients[client_id]
            
    async def send_message(self, client_id: str, message: Dict[str, Any]):
        """Send a message to a specific client"""
        if client_id in self.clients:
            try:
                await self.clients[client_id].send(json.dumps(message))
            except:
                await self.unregister_client(client_id)
                
    async def broadcast_message(self, message: Dict[str, Any]):
        """Broadcast a message to all clients"""
        if self.clients:
            disconnected_clients = []
            for client_id, websocket in self.clients.items():
                try:
                    await websocket.send(json.dumps(message))
                except:
                    disconnected_clients.append(client_id)
                    
            # Remove disconnected clients
            for client_id in disconnected_clients:
                await self.unregister_client(client_id)
    
    async def execute_command(self, client_id: str, command: str, cwd: Optional[str] = None) -> str:
        """Execute a command and stream output to client"""
        process_id = secrets.token_urlsafe(8)
        
        # Send start event
        await self.send_message(client_id, {
            "type": "start",
            "process_id": process_id,
            "command": command,
            "timestamp": datetime.now().isoformat()
        })
        
        try:
            # Start the process
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=cwd or os.getcwd(),
                universal_newlines=True,
                bufsize=1
            )
            
            self.processes[process_id] = process
            
            # Stream output
            while process.poll() is None:
                # Read stdout
                if process.stdout:
                    output = process.stdout.readline()
                    if output:
                        await self.send_message(client_id, {
                            "type": "output",
                            "process_id": process_id,
                            "data": output.strip(),
                            "stream": "stdout",
                            "timestamp": datetime.now().isoformat()
                        })
                
                # Read stderr
                if process.stderr:
                    error = process.stderr.readline()
                    if error:
                        await self.send_message(client_id, {
                            "type": "output",
                            "process_id": process_id,
                            "data": error.strip(),
                            "stream": "stderr",
                            "timestamp": datetime.now().isoformat()
                        })
                
                # Small delay to prevent busy waiting
                await asyncio.sleep(0.1)
                    
            # Send completion event
            exit_code = process.returncode
            await self.send_message(client_id, {
                "type": "complete",
                "process_id": process_id,
                "exit_code": exit_code,
                "timestamp": datetime.now().isoformat()
            })
            
            # Clean up
            if process_id in self.processes:
                del self.processes[process_id]
                
            return f"Command completed with exit code {exit_code}"
            
        except Exception as e:
            await self.send_message(client_id, {
                "type": "error",
                "process_id": process_id,
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            })
            
            if process_id in self.processes:
                del self.processes[process_id]
                
            return f"Command failed: {str(e)}"
    
    async def handle_client(self, websocket: Any):
        """Handle a client connection"""
        client_id = None
        try:
            # Wait for authentication
            auth_message = await websocket.recv()
            auth_data = json.loads(auth_message)
            
            if auth_data.get("type") != "auth":
                await websocket.close(1008, "Authentication required")
                return
                
            token = auth_data.get("token")
            client_id = await self.register_client(websocket, token)
            
            if not client_id:
                return
                
            # Send welcome message
            await self.send_message(client_id, {
                "type": "welcome",
                "message": "Connected to CoreX Agent",
                "timestamp": datetime.now().isoformat()
            })
            
            # Handle messages from client
            async for message in websocket:
                try:
                    data = json.loads(message)
                    message_type = data.get("type")
                    
                    if message_type == "execute":
                        command = data.get("command", "")
                        cwd = data.get("cwd")
                        # Run in a separate thread to avoid blocking
                        loop = asyncio.get_event_loop()
                        loop.run_in_executor(None, lambda: asyncio.run(self.execute_command(client_id, command, cwd)))
                        
                    elif message_type == "cancel":
                        process_id = data.get("process_id")
                        if process_id in self.processes:
                            self.processes[process_id].terminate()
                            await self.send_message(client_id, {
                                "type": "cancelled",
                                "process_id": process_id,
                                "timestamp": datetime.now().isoformat()
                            })
                            
                except json.JSONDecodeError:
                    await self.send_message(client_id, {
                        "type": "error",
                        "message": "Invalid JSON message",
                        "timestamp": datetime.now().isoformat()
                    })
                    
        except:
            pass
        finally:
            if client_id:
                await self.unregister_client(client_id)
    
    def generate_token(self) -> str:
        """Generate a new authentication token"""
        token = secrets.token_urlsafe(32)
        token_id = secrets.token_urlsafe(8)
        self.tokens[token_id] = token
        return token
    
    def save_token(self, token: str, filepath: str = ".corex_token"):
        """Save token to file for GUI authentication"""
        with open(filepath, "w") as f:
            f.write(token)
    
    async def start(self):
        """Start the WebSocket server"""
        print(f"Starting CoreX Agent on {self.host}:{self.port}")
        
        # Generate and save authentication token
        token = self.generate_token()
        self.save_token(token)
        print(f"Authentication token saved to .corex_token")
        print(f"Token: {token}")
        
        # Start server
        async with websockets.serve(self.handle_client, self.host, self.port):
            print("CoreX Agent is running...")
            await asyncio.Future()  # Run forever


def main():
    """Main entry point for CoreX Agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CoreX Agent - CLI↔GUI Synchronization Server")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8765, help="Port to bind to")
    
    args = parser.parse_args()
    
    agent = CoreXAgent(args.host, args.port)
    
    try:
        asyncio.run(agent.start())
    except KeyboardInterrupt:
        print("\nShutting down CoreX Agent...")
        sys.exit(0)


if __name__ == "__main__":
    main()