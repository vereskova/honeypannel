import json
from collections import Counter
from datetime import datetime

LOG_FILE = "logs/requests.jsonl"

RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
GREEN = "\033[92m"
RESET = "\033[0m"

def classify(event):
    path = event["path"]

    if path == "/.env":
        return "Secrets probing", YELLOW
    if "admin" in path:
        return "Admin panel access", RED
    if path.startswith("/api"):
        return "API reconnaissance", BLUE
    if path.endswith(".php"):
        return "PHP endpoint probing", RED

    return "Generic request", GREEN

path_counter = Counter()
total_events = 0

print("\n=== Honeypot Events ===\n")

with open(LOG_FILE, "r", encoding="utf-8") as f:
    for line in f:
        event = json.loads(line)
        total_events += 1

        ts = event["ts"]
        ip = event["client_ip"]
        method = event["method"]
        path = event["path"]

        label, color = classify(event)
        path_counter[path] += 1

        print(
            f"{color}"
            f"[{ts}] {ip} → {method} {path} | {label}"
            f"{RESET}"
        )
print("\n================== Statistics ======================\n")
print(f"Total events: {total_events}\n")

print("Top paths:")
for path, count in path_counter.most_common(10):
    print(f"  {path:<20} {count}")
