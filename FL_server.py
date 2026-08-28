"""
Federated Learning Cloud Server with Aggregation & DNA Encryption
"""

import numpy as np
import torch
import torch.nn as nn
import time
from collections import OrderedDict
from DNA_crypto import encrypt_weights, decrypt_weights

class FLServer:
    def __init__(self, global_model, password, rule=2, x0=0.42):
        self.model = global_model
        self.password = password
        self.rule = rule
        self.x0 = x0
        self.r = 3.99

        self.updates = {}
        self.sample_counts = {}
        self.round_num = 0
        self.accuracies = []
        self.losses = []
        self.agg_times = []
        self.criterion = nn.CrossEntropyLoss()

    def receive_update(self, client_id, encrypted_weights, client_password, num_samples):
        weights = decrypt_weights(encrypted_weights, client_password)
        self.updates[client_id] = weights
        self.sample_counts[client_id] = num_samples

    def aggregate(self):
        self.round_num += 1
        start = time.time()

        if not self.updates:
            return None

        total_n = sum(self.sample_counts.values())
        first = list(self.updates.values())[0]
        averaged = OrderedDict()

        for name in first.keys():
            weighted_sum = None
            for cid, weights in self.updates.items():
                n_k = self.sample_counts[cid]
                contribution = (n_k / total_n) * weights[name]
                if weighted_sum is None:
                    weighted_sum = contribution
                else:
                    weighted_sum += contribution
            averaged[name] = weighted_sum

        state = OrderedDict()
        for name, w in averaged.items():
            state[name] = torch.tensor(w).float()
        self.model.load_state_dict(state)

        self.agg_times.append(time.time() - start)
        self.updates.clear()
        self.sample_counts.clear()
        return averaged

    def encrypt_global(self):
        weights = {name: param.cpu().detach().numpy() for name, param in self.model.state_dict().items()}
        return encrypt_weights(weights, self.password, self.rule, self.x0, self.r)

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
        acc = 100 * correct / total
        avg_loss = loss / len(test_loader)
        self.accuracies.append(acc)
        self.losses.append(avg_loss)
        return acc, avg_loss
