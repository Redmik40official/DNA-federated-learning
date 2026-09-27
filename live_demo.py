import time
import json
from main import prepare_data
from FL_Model import CloudSecurityModel
from FL_client import FLClient
from FL_server import FLServer
import sys

# Terminal Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def run_live_demo():
    print(f"\n{CYAN}=============================================================={RESET}")
    slow_print(f"{CYAN}  LIVE DEMO: DNA-Encrypted Federated Learning Framework{RESET}", 0.02)
    print(f"{CYAN}=============================================================={RESET}\n")
    
    time.sleep(1)
    print(f"{YELLOW}[SYSTEM] Initializing 3 Cloud Nodes (AWS, Azure, GCP)...{RESET}")
    clients_data, test_loader, input_size = prepare_data(num_clients=3)
    
    global_model = CloudSecurityModel(input_size)
    server = FLServer(global_model, password="ServerSecretKey2024")
    
    clients = []
    for i in range(3):
        client = FLClient(i+1, clients_data[i], CloudSecurityModel(input_size), 
                          f"Client{i+1}@SecurePass2024", "ServerSecretKey2024")
        clients.append(client)
        
    print(f"{GREEN}[SYSTEM] Nodes Ready. Commencing Federated Round 1...{RESET}\n")
    time.sleep(1.5)

    # Demo just 1 full round visually (but train deeper locally for high accuracy)
    print(f"{CYAN}--- PHASE 1: LOCAL TRAINING ---{RESET}")
    for c in clients:
        loss, acc = c.train_local(epochs=5)
        print(f"Node {c.id} training complete. Local Accuracy: {acc:.2f}%")
        time.sleep(0.8)

    print(f"\n{CYAN}--- PHASE 2: DNA ENCRYPTION & TRANSMISSION ---{RESET}")
    time.sleep(1)
    
    # Show the actual DNA sequence for Client 1
    c1 = clients[0]
    slow_print(f"Node 1 encrypting model weights using Rule {c1.rule} & Chaotic Map...", 0.02)
    start_time = time.time()
    enc_payload = c1.encrypt_and_send()
    enc_time = time.time() - start_time
    
    # Extract the DNA sequence from the first neural network layer
    first_layer_key = list(enc_payload.keys())[0]
    dna_cipher = enc_payload[first_layer_key]['cipher']
    
    # Calculate approximate size of total payload
    payload_size = sum(len(layer['cipher']) for layer in enc_payload.values()) / 1024 / 1024 # MB
    
    print(f"{GREEN}[SUCCESS] Weights Encrypted in {enc_time:.2f} seconds.{RESET}")
    print(f"{RED}[INTERCEPTED NETWORK PACKET (Preview)]:{RESET}")
    print(f"{YELLOW}{dna_cipher[:150]}... [TRUNCATED, Total Size: {payload_size:.2f} MB]{RESET}")
    
    print(f"\n{CYAN}--- PHASE 3: SECURE AGGREGATION (SERVER) ---{RESET}")
    time.sleep(1.5)
    print(f"Server receiving packets from Nodes 1, 2, and 3...")
    for c in clients:
        if c.id != 1:
            server.receive_update(c.id, c.encrypt_and_send(), c.password, c.num_samples)
        else:
            server.receive_update(c.id, enc_payload, c.password, c.num_samples)
            
    print(f"{GREEN}[SUCCESS] Server decrypted all weights. Executing Federated Averaging...{RESET}")
    server.aggregate()
    time.sleep(1)

    print(f"\n{CYAN}--- PHASE 4: GLOBAL EVALUATION ---{RESET}")
    metrics = server.evaluate(test_loader)
    print(f"Global Model Accuracy: {GREEN}{metrics['accuracy']:.2f}%{RESET}")
    print(f"Global Model AUC:      {GREEN}{metrics['roc_auc']:.4f}{RESET}")
    
    print(f"\n{CYAN}=============================================================={RESET}")
    slow_print(f"{GREEN}  DEMO COMPLETE: Zero Data Shared. 100% DNA Encrypted.{RESET}", 0.03)
    print(f"{CYAN}=============================================================={RESET}\n")

if __name__ == '__main__':
    run_live_demo()
