from datetime import datetime

# Functie om de tijd te parsen en om te zetten naar datetime object
def parse_time(time_str):
    return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")

# Data als voorbeeld (je kunt dit vervangen door de echte data in een bestand)
data = open("data.txt", "r")

# Functie om de tijdsverschillen voor een bepaalde test te berekenen
def calculate_time_diff(test_name, data):
    lines = data.strip().split('\n')
    
    test_creation_time = None
    deployments_services_times = []
    
    # Zoek de tijd voor de test (bijv. test1 of test2) en de bijbehorende deployments/services
    for line in lines:
        name, created = line.split()
        created_time = parse_time(created)
        
        if test_name in name and 'deployment' in name or 'service' in name:
            deployments_services_times.append(created_time)
        elif test_name == name:
            test_creation_time = created_time
    
    if test_creation_time is None:
        print(f"Test {test_name} niet gevonden.")
        return
    
    # Bereken de tijdsverschillen voor de deployments/services
    print(f"Tijd voor {test_name} en zijn deployments/services:")
    for time in deployments_services_times:
        time_diff = time - test_creation_time
        print(f"{test_name} -> Deployment/Service tijd: {time_diff}")

# Test voor test1
calculate_time_diff("test1", data)

# Test voor test2
calculate_time_diff("test2", data)
