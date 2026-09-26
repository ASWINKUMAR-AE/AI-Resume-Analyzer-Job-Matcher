import os
import sys
import subprocess
import time
import webbrowser
import socket

def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.STREAM if hasattr(socket, 'STREAM') else socket.SOCK_STREAM) as s:
        s.settimeout(2)
        return s.connect_ex((host, port)) == 0

def get_python_cmd():
    # Check virtual environment python first
    root = os.path.dirname(os.path.abspath(__file__))
    venv_py = os.path.join(root, "backend", "venv", "Scripts", "python.exe")
    if os.path.exists(venv_py):
        return venv_py
    
    # Try sys.executable
    if sys.executable and os.path.exists(sys.executable):
        return sys.executable
    return "py"

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    print("======================================================================")
    print("          AI RESUME ANALYZER & JOB MATCHER - LAUNCHER")
    print("======================================================================")

    # 1. Check MySQL
    print("[*] Checking XAMPP MySQL server at localhost:3306...")
    if not check_port("127.0.0.1", 3306):
        print("\n[!] ERROR: MySQL is not reachable on localhost:3306.")
        print("[!] Please start MySQL from your XAMPP Control Panel and try again.\n")
        sys.exit(1)
    print("[+] MySQL is running.")

    # 2. Virtual environment setup
    venv_py = os.path.join(root, "backend", "venv", "Scripts", "python.exe")
    if not os.path.exists(venv_py):
        print("[*] Creating backend virtual environment...")
        base_py = sys.executable if sys.executable else "py"
        subprocess.run([base_py, "-m", "venv", os.path.join(root, "backend", "venv")], check=True)

    print("[*] Verifying backend dependencies...")
    subprocess.run([venv_py, "-m", "pip", "install", "-q", "-r", os.path.join(root, "backend", "requirements.txt")], check=True)

    # 3. Database initialization
    print("[*] Verifying & seeding MySQL database...")
    subprocess.run([venv_py, os.path.join(root, "backend", "init_db.py"), "--seed"], check=True)

    # 4. Frontend dependencies check
    if not os.path.exists(os.path.join(root, "frontend", "node_modules")):
        print("[*] Installing frontend dependencies...")
        subprocess.run(["npm", "install"], cwd=os.path.join(root, "frontend"), shell=True, check=True)

    # 5. Launch Backend and Frontend
    print("[*] Launching Backend Flask server on http://127.0.0.1:5000...")
    backend_proc = subprocess.Popen([venv_py, "app.py"], cwd=os.path.join(root, "backend"))

    print("[*] Launching Frontend Vite server on http://localhost:5173...")
    frontend_proc = subprocess.Popen(["npm", "run", "dev"], cwd=os.path.join(root, "frontend"), shell=True)

    time.sleep(3)
    print("[*] Opening browser at http://localhost:5173...")
    webbrowser.open("http://localhost:5173")

    print("\n======================================================================")
    print("  SUCCESS! Full-Stack Application is Live:")
    print("  - Web App:  http://localhost:5173")
    print("  - REST API: http://127.0.0.1:5000")
    print("  - Database: XAMPP MySQL (ai_resume_matcher)")
    print("\n  Demo Accounts:")
    print("  - Student: alex.student@example.com / Student@123")
    print("  - Company: hr@technova.com / Company@123")
    print("  - Admin:   admin@airesume.com / Admin@123")
    print("\n  Press CTRL+C in this terminal to stop all servers.")
    print("======================================================================\n")

    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\n[*] Stopping servers...")
        backend_proc.terminate()
        frontend_proc.terminate()
        print("[+] Servers stopped.")

if __name__ == "__main__":
    main()
