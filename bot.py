import requests
import random
import threading
from datetime import datetime

YOUR_REF_CODE = "Hacker1"
YOUR_USERNAME = "Hacker1"
YOUR_PASSWORD = "MIzero250@"  # ← REPLACE
TONKING_API = "https://tonking.io/api"

def quick_claim(i):
    # Register + claim in one go
    user = f"ghost_{random.randint(100000, 999999)}"
    pwd = "GhostPass!2025"
    reg = requests.post(f"{TONKING_API}/register", json={"username": user, "password": pwd, "ref": YOUR_REF_CODE}, timeout=5)
    if reg.status_code == 200:
        token = reg.json().get("token")
        if token:
            requests.post(f"{TONKING_API}/faucet/claim", headers={"Authorization": f"Bearer {token}"}, timeout=5)

# Keep your account alive
requests.post(f"{TONKING_API}/login", json={"username": YOUR_USERNAME, "password": YOUR_PASSWORD})

# Run 50 threads (fast)
threads = []
for i in range(50):
    t = threading.Thread(target=quick_claim, args=(i,))
    threads.append(t)
    t.start()

# Wait max 50 seconds
for t in threads:
    t.join(timeout=1)

print(f"[✅] {datetime.now()} | Hourly run complete")
