# DNA-Encrypted Federated Learning for Cloud Security

This repository contains the proof-of-concept implementation of a quantum-resistant cloud security framework integrating **DNA Cryptography** with **Federated Learning (FL)**.

## Overview
As quantum computing threatens traditional mathematical encryption (RSA/AES), this project explores a post-quantum alternative. By combining the biological complexity of DNA sequences with the decentralized privacy of Federated Learning, this system allows multiple cloud nodes (e.g., AWS, Azure, GCP) to train a global AI model without ever sharing raw data or relying on prime-factorization encryption.

### Key Features
*   **Federated Learning:** Decentralized AI training using PyTorch.
*   **DNA Cryptography Integration:** Model weights are encrypted using A, C, G, T encoding, Logistic Chaotic Maps, and multi-layer biological operations (XOR/ADD) before transmission.
*   **Zero Data Sharing:** Raw data never leaves the local client node.
*   **Quantum-Resistant Principles:** Does not rely on mathematical structures vulnerable to Shor's Algorithm.

## Repository Structure
*   `main.py`: The entry point. Orchestrates the federated training loop across the simulated clients and server.
*   `DNA_crypto.py`: The core encryption engine. Handles text-to-DNA conversion, chaotic sequence generation, and weight encryption/decryption.
*   `FL_server.py`: The central aggregator node using weighted FedAvg.
*   `FL_client.py`: The local client nodes that train on local data and encrypt updates.
*   `FL_Model.py`: The PyTorch Neural Network architecture (CloudSecurityModel).
*   `generate_report.py`: Script to generate publication-quality visual charts of the training metrics.

## Performance Metrics (Breast Cancer Dataset Simulation)
After 10 federated rounds across 3 simulated cloud clients:
*   **Global Accuracy:** 83.33% → **97.37%**
*   **Final Loss:** 0.0727 (Converged rapidly by Round 3)
*   **Client Collaboration:** The weakest isolated node improved from 69.72% to 94.34% purely through encrypted federated intelligence transfer.

## Requirements
*   Python 3.8+
*   `torch`
*   `numpy`
*   `scikit-learn`
*   `matplotlib`

## Usage
1. Install dependencies: `pip install torch numpy scikit-learn matplotlib`
2. Run the simulation: `python main.py`
3. Generate metric charts: `python generate_report.py`

## Disclaimer
*This project is a foundational prototype (V1) built for research and proof-of-concept purposes. It integrates established DNA Cryptography concepts into an FL pipeline. Future work involves formal scaling and transitioning to standardized post-quantum frameworks (e.g., CRYSTALS-Kyber).*
