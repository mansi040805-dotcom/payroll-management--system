"""
run_system.py - One-command launcher for PaySphere Modern Web Application

Launches the Python OOP Backend and serves the React UI.
Usage:
    python run_system.py
"""

import os
import sys
import webbrowser
import threading
import time

def open_browser(port):
    time.sleep(1.5)
    url = f"http://localhost:{port}"
    print(f"\n[Browser] Opening PaySphere Web App at {url} ...\n")
    try:
        webbrowser.open(url)
    except Exception:
        pass

def main():
    print("=" * 65)
    print("  PAYSPHERE — MODERN OOP PAYROLL & COMPENSATION SYSTEM")
    print("=" * 65)
    print("  Initializing Python OOP domain engine & JSON records...")
    
    from api_server import app, create_sample_data
    create_sample_data()

    port = int(os.environ.get("PORT", 5000))
    print(f"\n  [Backend]  REST API running on http://127.0.0.1:{port}/api")
    print(f"  [Frontend] Web UI available on  http://localhost:{port}")
    print(f"  [Vite Dev] If developing: cd frontend && npm run dev (port 3000)")
    print("=" * 65)
    print("  Press Ctrl+C to stop the server.\n")

    # Automatically launch browser in background
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()

    app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    main()
