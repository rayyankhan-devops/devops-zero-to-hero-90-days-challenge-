#!/usr/bin/env python3
# ==============================================================================
# Script Name: api_server.py
# Description: Run a lightweight, zero-dependency REST HTTP JSON API server.
#              Perfect for system design and API request-response practice.
# Author:      Muhammad Rayyan
# ==============================================================================

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HOST = "127.0.0.1"
PORT = 8000

class DevOpsApiHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        # Override to suppress default console noise and format cleanly
        print(f"📡 API LOG - [{self.log_date_time_string()}] - Request: {args[0]}")

    def do_GET(self):
        # Route handler
        if self.path == "/" or self.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            response = {
                "status": "UP",
                "message": "DevOps API server is running healthily",
                "port": PORT
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
            
        elif self.path == "/api/users":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            users = [
                {"id": 1, "name": "Muhammad Rayyan", "role": "DevOps Lead"},
                {"id": 2, "name": "Alice", "role": "Site Reliability Engineer"},
                {"id": 3, "name": "Bob", "role": "Cloud Architect"}
            ]
            self.wfile.write(json.dumps(users).encode("utf-8"))
            
        else:
            # Resource not found routing
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            err = {"error": "NotFound", "message": f"Resource path '{self.path}' not found."}
            self.wfile.write(json.dumps(err).encode("utf-8"))

def run_server():
    server = HTTPServer((HOST, PORT), DevOpsApiHandler)
    print("============================================================")
    print(f"🟢 Server successfully listening on http://{HOST}:{PORT}")
    print("    Available Routes:")
    print(f"      - http://{HOST}:{PORT}/           (Health check)")
    print(f"      - http://{HOST}:{PORT}/api/users  (List users)")
    print("    Press Ctrl+C to stop the server.")
    print("============================================================")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping API server...")
        server.server_close()
        print("Server stopped.")

if __name__ == "__main__":
    run_server()
