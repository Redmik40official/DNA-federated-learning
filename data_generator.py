import pandas as pd
import numpy as np
import os

def generate_threat_data(num_samples=1000, output_file='threat_data.csv'):
    np.random.seed(42)
    
    # 1. Generate Input Features (Threat Metrics)
    # CPU Load (0 to 100%)
    cpu_load = np.random.uniform(10, 99, num_samples)
    # Failed logins in last minute (0 to 50)
    failed_logins = np.random.poisson(lam=2, size=num_samples) 
    failed_logins[failed_logins > 50] = 50
    # Network traffic MB/s (10 to 1000)
    network_traffic = np.random.uniform(10, 1000, num_samples)
    # Ping latency ms (10 to 500)
    latency = np.random.uniform(10, 500, num_samples)

    # 2. Determine target labels (DNA Crypto parameters) based on rules
    # Rule ID (1 to 4)
    # Key Length (128, 256, 512, 1024) - Let's map this to classes 0, 1, 2, 3 for PyTorch
    
    mapping_rules = []
    key_length_classes = []
    
    for i in range(num_samples):
        threat_score = (cpu_load[i]/100) + (failed_logins[i]/10) + (network_traffic[i]/1000)
        
        if threat_score < 1.0:
            # Low Threat
            mapping_rules.append(0) # Rule 1 (0-indexed)
            key_length_classes.append(0) # 128
        elif threat_score < 2.0:
            # Medium Threat
            mapping_rules.append(1) # Rule 2
            key_length_classes.append(1) # 256
        elif threat_score < 3.0:
            # High Threat
            mapping_rules.append(2) # Rule 3
            key_length_classes.append(2) # 512
        else:
            # Critical Threat
            mapping_rules.append(3) # Rule 4
            key_length_classes.append(3) # 1024
            
    # Create DataFrame
    df = pd.DataFrame({
        'cpu_load': cpu_load,
        'failed_logins': failed_logins,
        'network_traffic': network_traffic,
        'latency': latency,
        'target_mapping_rule': mapping_rules,
        'target_key_length': key_length_classes
    })
    
    df.to_csv(output_file, index=False)
    print(f"Generated {num_samples} samples and saved to {output_file}")

if __name__ == "__main__":
    # Generate data for AWS node
    generate_threat_data(1000, 'aws_threat_logs.csv')
    # Generate data for Azure node
    generate_threat_data(1000, 'azure_threat_logs.csv')
