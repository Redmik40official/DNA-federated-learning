# DNA-Encrypted Federated Learning Framework (V2: Enterprise Zero-Trust)

This repository contains the proof-of-concept implementation of a quantum-resistant cloud security framework integrating **DNA Cryptography** with **Federated Learning (FL)**, upgraded with Enterprise Zero-Trust features.

## 🚀 V2 Upgrades (Enterprise Architecture)
*   **Interactive Streamlit UI:** A complete real-time dashboard visualizing distributed training, cryptographic integrity, and live network threat detection.
*   **Local Differential Privacy (LDP):** Injects Gaussian noise into client weights prior to encryption, preventing Model Inversion attacks from an honest-but-curious server.
*   **Non-IID Data Handling:** Implements **FedProx** to handle heterogeneous cloud data distributions (simulated via Dirichlet splitting).
*   **Deep Training Setup:** Cosine Annealing Learning Rate scheduler applied over 50,000 simulated cloud network logs.

## 🧠 Overview
As quantum computing threatens traditional encryption (RSA/ECC) via Shor's Algorithm (the "Harvest Now, Decrypt Later" threat), this project explores a post-quantum alternative. By combining the biological complexity of DNA sequences (A, C, G, T) with the decentralized privacy of Federated Learning, multiple cloud nodes (AWS, Azure, GCP) train a global AI model without sharing raw data.

### Key Features
*   **Federated Learning:** Decentralized AI training using PyTorch.
*   **DNA Cryptography Integration:** Model weights are encrypted using A, C, G, T encoding, Logistic Chaotic Maps, and multi-layer biological operations (XOR/ADD) before transmission.
*   **Quantum-Resistant:** Does not rely on algebraic mathematical structures vulnerable to Shor's Algorithm.
*   **Cryptographic Verification:** Lossless encryption verified via layer-by-layer SHA-256 checksums.

## 📊 Performance Metrics (20 Federated Rounds)
*   **Global Accuracy:** 98.88%
*   **F1-Score:** 96.29%
*   **ROC-AUC:** 0.9869
*   **Fault Tolerance:** Survived 9 simulated network dropout events with zero degradation.

## 💻 Usage
1. Install dependencies: `pip install torch numpy scikit-learn matplotlib pandas streamlit seaborn`
2. Run the interactive dashboard: `python -m streamlit run app.py`

## Disclaimer
*This project is a V2 prototype built for academic research. It demonstrates a theoretical integration of biological encryption principles with collaborative AI to mitigate post-quantum threats.*
