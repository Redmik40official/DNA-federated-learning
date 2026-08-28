"""
Enhanced DNA Cryptography using Federated Learning for Cloud Data Security
Main Execution Entrypoint
"""

import os
import sys
import torch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import time

# Fix Windows terminal Unicode encoding
sys.stdout.reconfigure(encoding='utf-8')

from FL_Model import CloudSecurityModel
from FL_client import FLClient
from FL_server import FLServer
from DNA_crypto import encrypt, decrypt

os.makedirs('results', exist_ok=True)

def prepare_data(num_clients=3):
    print("\n📂 Loading Dataset (Breast Cancer)...")
    data = load_breast_cancer()
    X, y = data.data, data.target

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    split = len(X_train) // num_clients
    clients_data = []

    for i in range(num_clients):
        s = i * split
        e = s + split if i < num_clients - 1 else len(X_train)
        Xc = torch.FloatTensor(X_train[s:e])
        yc = torch.LongTensor(y_train[s:e])
        loader = DataLoader(TensorDataset(Xc, yc), batch_size=32, shuffle=True)
        clients_data.append(loader)

    Xt = torch.FloatTensor(X_test)
    yt = torch.LongTensor(y_test)
    test_loader = DataLoader(TensorDataset(Xt, yt), batch_size=32)

    return clients_data, test_loader, X.shape[1]

def run_federated_learning(num_clients=3, num_rounds=10, local_epochs=3):
    clients_data, test_loader, input_size = prepare_data(num_clients)

    global_model = CloudSecurityModel(input_size)
    server = FLServer(global_model=global_model, password="ServerSecretKey2024", rule=2, x0=0.42)

    clients = []
    for i in range(num_clients):
        model = CloudSecurityModel(input_size)
        client = FLClient(
            client_id=i + 1,
            dataloader=clients_data[i],
            model=model,
            password=f"Client{i+1}@SecurePass2024",
            server_password="ServerSecretKey2024",
            lr=0.001,
            rule=(i % 8) + 1,
            x0=round(0.2 + i * 0.2, 2)
        )
        clients.append(client)

    round_accuracies = []
    round_losses = []

    for rnd in range(1, num_rounds + 1):
        print(f"\n── FL ROUND {rnd}/{num_rounds} ──")

        # 1. Local Training
        for c in clients:
            loss, acc = c.train_local(epochs=local_epochs)
            print(f"   [Client {c.id}] Loss: {loss:.4f} | Local Acc: {acc:.2f}%")

        # 2. DNA Encryption & Transmission
        for c in clients:
            enc_weights = c.encrypt_and_send()
            server.receive_update(c.id, enc_weights, c.password, c.num_samples)

        # 3. Server FedAvg
        server.aggregate()

        # 4. Global Encryption & Distribution
        enc_global = server.encrypt_global()
        for c in clients:
            c.receive_and_decrypt(enc_global)

        # 5. Evaluation
        acc, loss = server.evaluate(test_loader)
        round_accuracies.append(acc)
        round_losses.append(loss)
        print(f"   [Global Model] Accuracy: {acc:.2f}% | Loss: {loss:.4f}")

    # Plot metrics
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, num_rounds + 1), round_accuracies, 'b-o')
    plt.title('Global Model Accuracy (%)')
    plt.xlabel('Round')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(range(1, num_rounds + 1), round_losses, 'r-o')
    plt.title('Global Model Loss')
    plt.xlabel('Round')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('results/fl_dna_results.png')
    print("\n📊 Visual report generated at: results/fl_dna_results.png")
    return round_accuracies, round_losses

if __name__ == '__main__':
    print("═"*60)
    print("  Enhanced DNA Cryptography using Federated Learning")
    print("═"*60)
    run_federated_learning()
