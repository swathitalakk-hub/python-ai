"""
Lightweight Web Dashboard Server for Student Performance Analytics System.
"""
import http.server
import socketserver
import webbrowser
import os

PORT = 8080
DIRECTORY = os.path.join(os.path.dirname(__file__), "dashboard")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    print(f"[*] Starting Student Performance Analytics Dashboard at http://localhost:{PORT}")
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("[+] Dashboard online! Press Ctrl+C to stop.")
            webbrowser.open(f"http://localhost:{PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server shutdown gracefully.")
    except OSError:
        print(f"[!] Port {PORT} is busy. Opening file directly in default browser...")
        index_file = os.path.abspath(os.path.join(DIRECTORY, "index.html"))
        webbrowser.open(f"file://{index_file}")

if __name__ == "__main__":
    start_server()
