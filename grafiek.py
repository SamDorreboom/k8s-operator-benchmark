import json
import matplotlib.pyplot as plt
from datetime import datetime

# Audit logs laden
audit_log_file = "test.log"

# Lijst om timestamps van requests op te slaan
timestamps = []

# Logs inlezen en timestamps extraheren
with open(audit_log_file, 'r') as f:
    for line in f:
        log = json.loads(line)
        if log.get("user", {}).get("username") == "system:serviceaccount:wordpress-operator-system:wordpress-operator-controller-manager":
            time_str = log["requestReceivedTimestamp"]
            timestamp = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")  # Exacte tijd
            timestamps.append(timestamp)

# Sorteer timestamps
timestamps.sort()

# Maak een cumulatieve teller
cumulative_requests = list(range(1, len(timestamps) + 1))

# Grafiek plotten
plt.figure(figsize=(12, 6))
plt.plot(timestamps, cumulative_requests, marker="o", linestyle="-", label="Cumulatief aantal requests")
plt.xlabel("Tijd")
plt.ylabel("Totaal aantal requests")
plt.title("Cumulatief aantal Kubernetes API requests door WordPress Operator")
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.show()
