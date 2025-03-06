import subprocess
import time
import pandas as pd
import matplotlib.pyplot as plt

namespace = "wordpress-operator-system"
pod_label = "control-plane=controller-manager"
output_file = "operator_resource_usage.csv"

# Zoek de juiste Pod op basis van de labelselector
pod_name_cmd = f"kubectl get pods -n {namespace} -l {pod_label} -o jsonpath='{{.items[0].metadata.name}}'"
pod_name = subprocess.getoutput(pod_name_cmd)

print(f"Monitoring resource usage for pod: {pod_name} in namespace: {namespace}")

# Data opslaan
data = []

for _ in range(30):  # 30 metingen (~5 min bij 10 sec interval)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Haal metrics op met kubectl top
        metrics = subprocess.getoutput(f"kubectl top pod {pod_name} -n {namespace} --no-headers")
        cpu, memory = metrics.split()[1:3]
        
        # Opslaan in lijst
        data.append([timestamp, int(cpu.strip('m')), int(memory.strip('Mi'))])
        print(f"{timestamp} - CPU: {cpu}m, Memory: {memory}Mi")
    
    except Exception as e:
        print(f"Fout bij ophalen van metrics: {e}")

    time.sleep(10)  # Interval van 10 seconden

# Dataframe aanmaken en opslaan als CSV
df = pd.DataFrame(data, columns=["Timestamp", "CPU (mCPU)", "Memory (MiB)"])
df.to_csv(output_file, index=False)
print(f"Monitoring completed. Results saved in {output_file}")

# Grafiek plotten
plt.figure(figsize=(10, 5))
plt.plot(df["Timestamp"], df["CPU (mCPU)"], marker="o", linestyle="-", label="CPU (mCPU)")
plt.plot(df["Timestamp"], df["Memory (MiB)"], marker="s", linestyle="-", label="Memory (MiB)")
plt.xlabel("Tijd")
plt.ylabel("Resource Gebruik")
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.title("Kubernetes Operator Resource Gebruik")
plt.show()
