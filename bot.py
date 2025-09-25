import requests
import random
import time
import threading
from datetime import datetime

# === 🔑 YOUR CONFIG ===
YOUR_REF_CODE = "Hacker1"          # From your link: https://tonking.io/?ref=Hacker1
YOUR_USERNAME = "Hacker1"          # Your real tonking.io username
YOUR_PASSWORD = "MIZero250@"  # ← REPLACE THIS WITH YOUR ACTUAL PASSWORD

TONKING_API = "https://tonking.io/api"
FAUCET_INTERVAL = 3600  # 1 hour
TOTAL_USERS = 100       # Start with 100 fake users

fake_users = []

def register_fake_user(i):
    username = f"ghost_{random.randint(100000, 999999)}"
    password = "GhostPass!2025"
    
    payload = {
        "username": username,
        "password": password,
        "ref": YOUR_REF_CODE
    }
    
    try:
        r = requests.post(f"{TONKING_API}/register", json=payload, timeout=10)
        if r.status_code == 200 and "token" in r.text:
            token = r.json()["token"]
            fake_users.append({"username": username, "token": token})
            print(f"[✅] {datetime.now()} | Registered {username}")
            return True
        else:
            print(f"[❌] {datetime.now()} | Failed {username} | Status: {r.status_code}")
            return False
    except Exception as e:
        print(f"[⚠️] {datetime.now()} | Error: {e}")
        return False

def claim_faucet(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.post(f"{TONKING_API}/faucet/claim", headers=headers, timeout=10)
        if r.status_code == 200:
            reward = r.json().get("reward", 0)
            print(f"[💰] {datetime.now()} | Claimed {reward} TON (you get 50%)")
        else:
            print(f"[⚠️] Faucet failed: {r.status_code}")
    except Exception as e:
        print(f"[⚠️] Faucet error: {e}")

def keep_your_account_alive():
    """Prevent 7-day commission reset"""
    payload = {"username": YOUR_USERNAME, "password": YOUR_PASSWORD}
    try:
        r = requests.post(f"{TONKING_API}/login", json=payload)
        if r.status_code == 200:
            print(f"[🛡️] {datetime.now()} | Your account is ALIVE — commission safe")
        else:
            print(f"[🔥] {datetime.now()} | WARNING: Your account may reset!")
    except Exception as e:
        print(f"[🔥] Keep-alive error: {e}")

# === 🚀 MAIN EXECUTION ===
if __name__ == "__main__":
    print(f"[🤖] {datetime.now()} | TONKING GHOST BOT — DEPLOYED ON RENDER")
    
    # Step 1: Keep YOUR account alive
    keep_your_account_alive()
    
    # Step 2: Register fake users
    print(f"[👥] Registering {TOTAL_USERS} fake users...")
    threads = []
    for i in range(TOTAL_USERS):
        t = threading.Thread(target=register_fake_user, args=(i,))
        threads.append(t)
        t.start()
        time.sleep(0.3)  # Avoid rate limits
    
    for t in threads:
        t.join()
    
    print(f"[✅] {len(fake_users)} fake users ready")
    
    # Step 3: Claim faucet for 24 hours (Render wakes daily)
    for hour in range(24):
        print(f"\n[⏰] Hour {hour+1}/24 — claiming faucets...")
        claim_threads = []
        for user in fake_users:
            t = threading.Thread(target=claim_faucet, args=(user["token"],))
            claim_threads.append(t)
            t.start()
        for t in claim_threads:
            t.join()
        print(f"[💤] Sleeping 1 hour...")
        time.sleep(FAUCET_INTERVAL)
    
    print(f"[🔚] Bot cycle complete — Render will restart tomorrow")