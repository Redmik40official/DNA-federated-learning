# DNA-Encrypted Federated Learning Project Analysis

**Analysis date:** 11 October 2026  
**Repository:** DNA Federated Learning  
**Project type:** Python research prototype with an interactive Streamlit dashboard

## 1. Executive summary

This project demonstrates a privacy-oriented federated-learning workflow for simulated cloud
network intrusion detection. Three simulated cloud clients train local PyTorch models. Client
model weights are converted into JSON, encoded as DNA bases (`A`, `C`, `G`, `T`), transformed
with a password-derived key and a logistic chaotic sequence, and sent to a custom aggregation
server. The server performs weighted federated averaging and distributes an encrypted global
model back to active clients.

The project also includes:

- A Streamlit dashboard for training, threat-detection demonstrations, and encryption checks.
- A custom multilayer perceptron for binary intrusion classification.
- FedProx-style proximal regularization for local client training.
- Gaussian noise injection before weight encryption, described in the code as local
  differential privacy.
- Synthetic data generation, metric plotting, logging, and saved PyTorch model artifacts.

The repository is best described as an **academic proof of concept**, not a production
federated-learning or post-quantum cryptography framework. The federated protocol and DNA
encryption are implemented in project code rather than supplied by a dedicated FL or
cryptography framework.

## 2. Frameworks and major technologies

### Primary frameworks

| Technology | Role | Evidence |
|---|---|---|
| **PyTorch** | Neural-network definition, tensor operations, training, optimizers, model serialization, and data loaders | `FL_Model.py`, `FL_client.py`, `FL_server.py`, `main.py` |
| **Streamlit** | Interactive web dashboard with tabs, controls, progress indicators, charts, downloads, and live demonstrations | `app.py` |
| **scikit-learn** | Synthetic classification data, scaling, train/test splitting, and accuracy/F1/ROC-AUC/confusion-matrix metrics | `main.py`, `FL_server.py`, `app.py` |
| **NumPy** | Numerical arrays, random data/noise generation, reshaping, and chaotic-sequence processing | `DNA_crypto.py`, `FL_client.py`, `main.py` |
| **pandas** | Threat-log DataFrame creation and CSV export | `data_generator.py`, `app.py` |
| **Matplotlib** | Training curves and result visualizations | `main.py`, `generate_report.py`, `generate_linkedin_cards.py`, `app.py` |
| **Seaborn** | Confusion-matrix heatmap styling in the dashboard | `app.py` |
| **python-docx** | Optional generation of Word-format project documentation | `generate_docx.py` |

### Important non-framework components

- **Custom federated-learning implementation:** `FLClient` and `FLServer` implement local
  training, update exchange, weighted aggregation, and global-model distribution. No
  `flwr`/Flower, FedML, TensorFlow Federated, or PySyft dependency is present.
- **Custom DNA transformation module:** `DNA_crypto.py` implements binary-to-DNA mappings,
  DNA XOR/add/substitution tables, SHA-256-derived material, logistic-map sequences, and
  weight serialization. It is not a standard or independently verified cryptographic library.
- **Python standard library:** `json`, `hashlib`, `logging`, `random`, `time`, `os`, `sys`,
  and `collections.OrderedDict` support serialization, hashing, logging, timing, and runtime
  behavior.

## 3. Architecture

```text
Synthetic intrusion data
        |
        v
prepare_data() in main.py
        |
        +--> 3 client DataLoaders with deliberately different class distributions
        |
        v
CloudSecurityModel (PyTorch MLP)
        |
        +--> FLClient: local training + FedProx term + Gaussian weight noise
        |        |
        |        +--> DNA_crypto.encrypt_weights()
        |
        v
FLServer: decrypt client updates + sample-weighted FedAvg
        |
        +--> encrypt_global()
        |
        v
Active clients receive and decrypt the global model
        |
        v
Evaluation, plots, logs, and saved .pth model
```

The dashboard in `app.py` exposes three user-facing areas:

1. Federated training simulation and convergence charts.
2. Simulated packet/threat classification.
3. DNA encryption and SHA-256 comparison demonstrations.

## 4. Machine-learning implementation

### Model

`CloudSecurityModel` is a PyTorch binary classifier with:

- 30 input features.
- Linear layers of 64 and 32 hidden units.
- Batch normalization.
- ReLU activations.
- Dropout of 0.3 and 0.2.
- A two-class output layer.

`neural_network.py` contains a separate `ThreatToDNAModel` with two output heads for
predicting a DNA mapping rule and key-length class. This model is not connected to the main
federated-training path.

### Data

The main training path creates **50,000 synthetic samples** with
`sklearn.datasets.make_classification`, 30 features, and an 85%/15% class weighting. It
standardizes the data and uses an 80%/20% train/test split.

The repository also contains `data_generator.py`, which creates small CSV threat logs with
four hand-designed features. Those CSVs are separate from the 30-feature dataset used by
`main.py`.

### Federated optimization

- Local optimization uses PyTorch Adam with cosine-annealing learning-rate scheduling.
- A FedProx-style proximal penalty is added when the current global parameters are supplied.
- The server performs sample-count-weighted model averaging, i.e. a FedAvg-style aggregation.
- A simulated 10% client dropout is applied per round.
- Gaussian noise is added to client weights before encryption.

The code calls this noise mechanism LDP, but it does not calculate or report an epsilon,
delta, clipping sensitivity, or a formal privacy budget. Therefore, the implementation
should be described as **noise injection inspired by LDP**, rather than a measured
differential-privacy guarantee.

## 5. Encryption and integrity implementation

The custom encryption flow in `DNA_crypto.py` is:

1. Convert plaintext text to binary.
2. Map pairs of bits to DNA bases using one of eight mapping rules.
3. Derive a repeated DNA key from a SHA-256 hash of the password.
4. Generate a DNA sequence from a logistic map.
5. Combine the password-derived and chaotic sequences with DNA XOR.
6. Apply DNA XOR and DNA addition to produce the cipher sequence.
7. Store the cipher, rule, chaotic parameters, and tensor shape.

Model tensors are flattened and JSON-serialized before this process and reconstructed after
decryption.

The dashboard computes SHA-256 values before and after round-tripping weights. This verifies
that the current implementation reconstructs the serialized tensors identically in the demo;
it does **not** provide authentication, tamper resistance, key exchange, or proof that the
scheme is post-quantum secure.

## 6. Generated outputs and supporting assets

The `results` directory contains generated or example artifacts, including:

- `secure_global_model.pth`: saved PyTorch model weights.
- `conference_metrics.json`: round accuracy/loss data.
- `federated_training.log`: training log output.
- PNG charts and presentation cards.
- DOCX documentation files.

The repository also includes research PDFs and a project image used as reference or
presentation material; they are not runtime dependencies of the training application.

## 7. Strengths

- Clear separation between model, client, server, and encryption modules.
- Reproducibility support through seeded Python, NumPy, and PyTorch randomness.
- Demonstrates the full FL lifecycle: local training, encrypted update transfer, aggregation,
  redistribution, and evaluation.
- Includes realistic prototype concerns such as non-IID client distributions and simulated
  client dropout.
- Provides a usable dashboard for demonstrations and visual inspection.
- Exports metrics, logs, figures, and a reusable model artifact.

## 8. Risks, limitations, and inconsistencies

### Security limitations

1. Credentials/passwords are embedded in source code and dashboard defaults. They should be
   moved to environment variables or a secrets manager and rotated.
2. The custom cipher has no authenticated-encryption mechanism, nonce/IV design, replay
   protection, or secure key exchange.
3. SHA-256 comparisons demonstrate integrity after a local round trip, but a plain digest is
   not a message-authentication code and cannot authenticate an untrusted sender.
4. The server receives client-specific passwords in the local API and decrypts each update;
   this is a simulation of transport protection, not secure aggregation.
5. The claim that the design is “quantum-resistant” is not established by the repository.
   DNA encoding and chaotic maps alone do not constitute a recognized post-quantum
   cryptographic construction.

### Engineering and research limitations

1. There is no dependency manifest such as `requirements.txt` or `pyproject.toml`, so the
   environment cannot be reproduced reliably from the repository alone.
2. There is no visible automated test suite or CI configuration.
3. Several comments and generated documentation describe results or data sources that do not
   exactly match every current execution path. Treat stored metrics and report claims as
   experiment artifacts until regenerated from a clean run.
4. The threat-detection dashboard generates random demonstration packets and pads manual
   inputs with random latent features; this is useful for UI demonstration but is not a
   validated packet-analysis pipeline.
5. `neural_network.py` and `data_generator.py` represent an additional experimental path and
   are not integrated with the main 30-feature federated model.
6. The project has no deployment configuration for actual AWS, Azure, or GCP nodes. Those
   providers are simulated as local clients.

## 9. Recommended next steps

### Priority 1: reproducibility and correctness

- Add a pinned `requirements.txt` or `pyproject.toml`.
- Add tests for DNA round trips, malformed payloads, tensor shapes/dtypes, aggregation,
  dropout behavior, and metric calculations.
- Add a clean experiment script that records configuration, seed, data hash, and actual
  results in one machine-readable file.
- Remove unused imports and reconcile documentation, comments, and generated metrics with
  the current code.

### Priority 2: security hardening

- Replace embedded credentials with environment-based secret loading.
- Use an established authenticated encryption or post-quantum cryptography design for
  production security; keep the DNA transform explicitly labeled as an experiment.
- Add sender authentication, replay protection, key rotation, and transport security.
- Implement formal secure aggregation if the server must not see individual updates.
- If differential privacy is a project requirement, add clipping, a formal mechanism, and
  epsilon/delta accounting.

### Priority 3: research validation

- Compare against plaintext FL, FedAvg, FedProx, and standard cryptographic baselines.
- Evaluate on a documented real or public intrusion-detection dataset.
- Report confidence intervals across multiple seeds rather than one run.
- Measure encryption/decryption overhead, payload expansion, dropout impact, and privacy/
  utility trade-offs.
- Add threat-model-specific attack evaluations, including update leakage and tampering.

## 10. Final assessment

The project successfully demonstrates an end-to-end educational prototype that combines
PyTorch classification, custom federated learning, custom DNA-based transformations, and a
Streamlit presentation layer. Its strongest contribution is the integrated demonstration and
modular structure. Its current evidence supports claims such as “simulated encrypted
federated training” and “DNA-inspired model-weight transformation.” It does not yet support
production claims of formally guaranteed differential privacy, secure aggregation, or
recognized post-quantum cryptographic security.
