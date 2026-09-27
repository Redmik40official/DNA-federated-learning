"""
Federated Learning Client with DNA Encryption
"""

import torch
import torch.nn as nn
import numpy as np
import time
from collections import OrderedDict
from DNA_crypto import encrypt_weights, decrypt_weights

class FLClient:
    def __init__(self, client_id, dataloader, model, password, server_password=None, lr=0.001, rule=None, x0=None):
        self.id = client_id
        self.data = dataloader
        self.model = model
        self.password = password
        self.server_password = server_password or password  # password used to decrypt server broadcasts
        self.rule = rule or (client_id % 8) + 1
        self.x0 = x0 or round(0.2 + client_id * 0.15, 2)
        self.r = 3.99

        self.optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer, T_max=10, eta_min=1e-5
        )
        self.criterion = nn.CrossEntropyLoss()

        self.num_samples = len(dataloader.dataset)
        self.losses = []
        self.accuracies = []
        self.encrypt_times = []
        self.decrypt_times = []

    def train_local(self, global_weights=None, epochs=3, mu=0.01):
        self.model.train()
        total_loss = 0
        correct = 0
        total = 0

        for _ in range(epochs):
            for X, y in self.data:
                self.optimizer.zero_grad()
                out = self.model(X)
                loss = self.criterion(out, y)
                
                # ── IMPROVEMENT 1: FedProx Proximal Term (Handles Non-IID) ──
                if global_weights is not None:
                    proximal_term = 0.0
                    for param, global_w in zip(self.model.parameters(), global_weights):
                        proximal_term += ((param - global_w) ** 2).sum()
                    loss += (mu / 2) * proximal_term

                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                self.optimizer.step()

                total_loss += loss.item()
                _, pred = torch.max(out, 1)
                correct += (pred == y).sum().item()
                total += y.size(0)

        avg_loss = total_loss / (epochs * len(self.data))
        acc = 100 * correct / total
        self.losses.append(avg_loss)
        self.accuracies.append(acc)
        self.scheduler.step()
        return avg_loss, acc

    def get_weights(self, apply_ldp=True, noise_scale=0.001):
        weights = {}
        for name, param in self.model.state_dict().items():
            w = param.cpu().detach().numpy()
            
            # ── IMPROVEMENT 2: Local Differential Privacy (LDP) ──
            if apply_ldp:
                noise = np.random.normal(0, noise_scale, w.shape)
                w = w + noise
                
            weights[name] = w
        return weights

    def set_weights(self, weights_dict):
        state = OrderedDict()
        for name, w in weights_dict.items():
            state[name] = torch.tensor(w).float()
        self.model.load_state_dict(state)

    def encrypt_and_send(self):
        weights = self.get_weights()
        start = time.time()
        encrypted = encrypt_weights(weights, self.password, self.rule, self.x0, self.r)
        self.encrypt_times.append(time.time() - start)
        return encrypted

    def receive_and_decrypt(self, encrypted_global):
        start = time.time()
        weights = decrypt_weights(encrypted_global, self.server_password)
        self.decrypt_times.append(time.time() - start)
        self.set_weights(weights)

    def evaluate(self, test_loader):
        self.model.eval()
        correct = 0
        total = 0
        loss = 0
        with torch.no_grad():
            for X, y in test_loader:
                out = self.model(X)
                loss += self.criterion(out, y).item()
                _, pred = torch.max(out, 1)
                correct += (pred == y).sum().item()
                total += y.size(0)
        return 100 * correct / total, loss / len(test_loader)
