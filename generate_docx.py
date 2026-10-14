import sys
sys.stdout.reconfigure(encoding='utf-8')

from docx import Document
from docx.shared import Pt, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

doc = Document()

# Standard A4 margins
section = doc.sections[0]
section.top_margin    = Cm(2.54)
section.bottom_margin = Cm(2.54)
section.left_margin   = Cm(3.17)
section.right_margin  = Cm(3.17)

# Default font
doc.styles['Normal'].font.name = 'Calibri'
doc.styles['Normal'].font.size = Pt(11)

def add_para(text, bold=False, italic=False, size=11, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.name = 'Calibri'
    run.font.size = Pt(size)
    return p

def add_heading(text, level=1):
    p = doc.add_heading(text, level=level)
    for run in p.runs:
        run.font.name = 'Calibri'
    return p

def add_code(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent  = Inches(0.3)
    p.paragraph_format.right_indent = Inches(0.3)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  'F2F2F2')
    pPr.append(shd)
    run = p.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(9)
    return p

def add_table(headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    hdr = table.rows[0]
    for i, h in enumerate(headers):
        hdr.cells[i].text = ''
        run = hdr.cells[i].paragraphs[0].add_run(h)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(10)
    for ri, row_data in enumerate(rows):
        row = table.rows[ri + 1]
        for ci, val in enumerate(row_data):
            row.cells[ci].text = val
            for run in row.cells[ci].paragraphs[0].runs:
                run.font.name = 'Calibri'
                run.font.size = Pt(10)
    return table

# ── TITLE ──────────────────────────────────────────────────────────────────────
t = doc.add_heading('DNA-Encrypted Federated Learning Framework', 0)
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_para('Architecture  |  Data Flow  |  Algorithms  |  Core Code',
         italic=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para('Author: Rakul Raj', size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para('Domain: Cloud Security, Post-Quantum Cryptography, Federated AI',
         size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para('GitHub: https://github.com/Redmik40official/DNA-federated-learning',
         size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_page_break()

# ── SECTION 1: ARCHITECTURE ────────────────────────────────────────────────────
add_heading('1. System Architecture', 1)
add_para(
    'The DNA-Encrypted Federated Learning (DNA-FL) framework is a three-tier distributed '
    'security architecture combining Post-Quantum Cryptography with Privacy-Preserving AI. '
    'It simulates a real-world multi-cloud environment across AWS, Azure, and GCP.')

doc.add_paragraph()
add_heading('1.1 Three-Tier Architecture Overview', 2)
add_table(
    ['Tier', 'Component', 'Role', 'Technology'],
    [
        ['Tier 1', 'Edge Client Nodes',     'Local AI Training on Private Data', 'PyTorch + FedProx + LDP'],
        ['Tier 2', 'DNA Encryption Engine', 'Biological Payload Encryption',     'Logistic Map + Watson-Crick Rules'],
        ['Tier 3', 'Central FL Server',     'Aggregation + Evaluation',          'Weighted FedAvg + Sklearn Metrics'],
    ]
)

doc.add_paragraph()
add_heading('1.2 Multi-Cloud Node Topology', 2)
add_code(
"""SYSTEM ARCHITECTURE TOPOLOGY
==============================

[AWS Cloud Node]            [Azure Cloud Node]          [GCP Cloud Node]
Client 1 - Rule 2           Client 2 - Rule 4           Client 3 - Rule 6
x0=0.4, Local Shard 1       x0=0.6, Local Shard 2       x0=0.8, Local Shard 3
(Non-IID: Mostly Normal)    (Non-IID: Mostly Attacks)   (Non-IID: Mixed)
      |                            |                           |
      v                            v                           v
[FedProx Local Training]    [FedProx Local Training]    [FedProx Local Training]
      |                            |                           |
      v                            v                           v
[LDP Noise Injection]       [LDP Noise Injection]       [LDP Noise Injection]
w_tilde = w + N(0,sigma^2)  Same                         Same
      |                            |                           |
      v                            v                           v
[DNA Encrypt Weights]       [DNA Encrypt Weights]       [DNA Encrypt Weights]
Cipher: ACGTGCAT...          Same                         Same
      |                            |                           |
      +----------------------------+---------------------------+
                                   |
                                   v
                       [Central FL Server]
                       1. Receive DNA Ciphertext Payloads
                       2. Decrypt using Client Passwords
                       3. Weighted FedAvg Aggregation
                       4. Evaluate Global Model
                       5. Broadcast Encrypted Global Weights
""")

doc.add_paragraph()
add_heading('1.3 Software Module Architecture', 2)
add_table(
    ['File', 'Module Role', 'Key Functions'],
    [
        ['DNA_crypto.py', 'Post-Quantum Encryption Engine',   'encrypt(), decrypt(), encrypt_weights(), decrypt_weights()'],
        ['FL_Model.py',   'Neural Network Architecture',      'CloudSecurityModel (MLP: 30 -> 64 -> 32 -> 2)'],
        ['FL_client.py',  'Autonomous Cloud Node Agent',      'train_local(), encrypt_and_send(), get_weights()'],
        ['FL_server.py',  'Aggregation and Evaluation Server','aggregate(), evaluate(), encrypt_global()'],
        ['main.py',       'Orchestration and Training Loop',  'prepare_data(), run_federated_learning(), set_seed()'],
        ['app.py',        'Interactive Streamlit Dashboard',  '3-Tab UI: Training, Inference, Crypto Verification'],
    ]
)
doc.add_page_break()

# ── SECTION 2: DATA FLOW ───────────────────────────────────────────────────────
add_heading('2. Data Flow', 1)

add_heading('2.1 Dataset Pipeline', 2)
add_table(
    ['Stage', 'Description', 'Output'],
    [
        ['Raw Generation',   'sklearn make_classification: 50,000 samples, 30 features',  'X (50000x30), y (50000,)'],
        ['Preprocessing',    'StandardScaler normalization (zero mean, unit variance)',     'X_scaled (50000x30)'],
        ['Train/Test Split', '80/20 split with random_state=42',                           '40,000 train | 10,000 test'],
        ['Non-IID Split',    'Dirichlet skew across 3 client nodes (alpha=0.5)',           '3 heterogeneous DataLoaders'],
        ['Tensor Convert',   'FloatTensor for features, LongTensor for labels',            'PyTorch DataLoader (batch=32)'],
    ]
)

doc.add_paragraph()
add_heading('2.2 Complete Round-by-Round Data Flow', 2)
add_code(
"""FEDERATED LEARNING ROUND DATA FLOW (Per Round t = 1 to 20)
============================================================

STEP 1: SERVER BROADCASTS GLOBAL MODEL
   Server encrypts global weights with ServerKey using DNA encryption.
   Sends DNA ciphertext to Client 1 (AWS), Client 2 (Azure), Client 3 (GCP).

STEP 2: CLIENTS DECRYPT GLOBAL MODEL
   Each client decrypts ciphertext using ServerKey -> w_global (float32 weights).

STEP 3: LOCAL FEDPROX TRAINING (5 epochs per client)
   Minimize: L = CrossEntropy(f(X_k), y_k) + (mu/2) * ||w - w_global||^2
     - X_k, y_k = Private local dataset shard (NEVER transmitted over network)
     - mu = 0.01

STEP 4: LOCAL DIFFERENTIAL PRIVACY NOISE INJECTION
   For each layer tensor w:
     w_noisy = w + N(0, sigma^2 * I)   [sigma = 0.001]

STEP 5: DNA ENCRYPTION OF LOCAL WEIGHTS
   Binary    = float32_to_bytes(w_noisy) -> bytes_to_binary()
   Plain_DNA = binary_to_dna(binary, rule=k)
   Key_pass  = make_key(ClientPassword, len(Plain_DNA))
   Key_chaos = chaotic_to_dna(logistic_map(x0, r=3.99, n=len))
   Combined  = DNA_XOR(Key_pass, Key_chaos)
   XOR_step  = DNA_XOR(Plain_DNA, Combined)
   Cipher    = DNA_ADD(XOR_step, Key_chaos)
   TRANSMIT: {cipher: ACGTGCAT..., rule: k, x0: client_x0, r: 3.99}

STEP 6: SERVER DECRYPTS RECEIVED WEIGHTS
   Server decrypts each client DNA payload using stored client passwords.

STEP 7: WEIGHTED FEDAVG AGGREGATION
   w_global = SUM( n_k / N_total * w_k )   for k in active_clients

STEP 8: SERVER EVALUATES ON TEST SET
   Computes: Accuracy, Precision, Recall, F1-Score, ROC-AUC

STEP 9: FAULT TOLERANCE
   10% random dropout probability per client per round.
   Server re-normalizes weights over remaining active clients only.
""")

doc.add_paragraph()
add_heading('2.3 DNA Encryption Data Flow (Single Weight Tensor)', 2)
add_code(
"""DNA ENCRYPTION PIPELINE (Single Weight Tensor)
================================================

INPUT: Weight Tensor, e.g., Linear layer [64, 30], dtype float32

Step 1 - Serialize:       Flatten -> JSON string "[0.234, -0.112, ...]"
Step 2 - Text to Binary:  Each char -> 8-bit ASCII binary
Step 3 - Binary to DNA:   Using Rule 2: 00->A, 01->G, 10->C, 11->T
Step 4 - Password Key:    SHA256(ClientPassword) -> Binary -> DNA (Rule 1)
Step 5 - Chaotic Key:     x(n+1) = 3.99 * x(n) * (1-x(n)), x0=0.4 -> DNA
Step 6 - Combined Key:    Key_combined = DNA_XOR(Key_password, Key_chaotic)
Step 7 - XOR Layer:       XOR_result = DNA_XOR(Plain_DNA, Key_combined)
Step 8 - ADD Layer:       Cipher = DNA_ADD(XOR_result, Key_chaotic)

OUTPUT: {cipher: "ACGTGCATGCAA...", rule: 2, x0: 0.4, r: 3.99, shape: [64,30]}
        Transmitted over network (Post-Quantum Protected Biological Payload)
""")
doc.add_page_break()

# ── SECTION 3: ALGORITHMS ──────────────────────────────────────────────────────
add_heading('3. Algorithms', 1)

add_heading('3.1 Logistic Chaotic Map (Key Generation)', 2)
add_para(
    'The Logistic Map generates a pseudo-random, non-repeating key sequence. '
    'For r = 3.99, the system exhibits full chaos with a positive Lyapunov exponent.')
add_code(
"""ALGORITHM: Logistic Map Key Generation
---------------------------------------
INPUT:  x0 (seed, 0.1 to 0.9), r = 3.99, n (number of bases)
OUTPUT: Chaotic DNA Key Sequence of length n

1. Initialize x = x0
2. For i = 1 to n:
     a. x = r * x * (1 - x)
     b. index = floor(x * 4) mod 4
     c. base = ['A','C','G','T'][index]
     d. Append base to key_sequence
3. Return key_sequence

Equation: x(n+1) = 3.99 * x(n) * (1 - x(n))
""")

doc.add_paragraph()
add_heading('3.2 DNA XOR and ADD Biological Operations', 2)
add_code(
"""DNA XOR Truth Table:
   A XOR A=A   A XOR C=C   A XOR G=G   A XOR T=T
   C XOR A=C   C XOR C=A   C XOR G=T   C XOR T=G
   G XOR A=G   G XOR C=T   G XOR G=A   G XOR T=C
   T XOR A=T   T XOR C=G   T XOR G=C   T XOR T=A

DNA ADD Table (Cyclic Modular Shift):
   A ADD A=A   A ADD C=C   A ADD G=G   A ADD T=T
   C ADD A=C   C ADD C=G   C ADD G=T   C ADD T=A
   G ADD A=G   G ADD C=T   G ADD G=A   G ADD T=C
   T ADD A=T   T ADD C=A   T ADD G=C   T ADD T=G
""")

doc.add_paragraph()
add_heading('3.3 FedProx Optimization Algorithm', 2)
add_code(
"""ALGORITHM: FedProx Local Client Training
------------------------------------------
INPUT:  Local dataset D_k, Global weights w_global, mu=0.01, epochs=5
OUTPUT: Updated local weights w_k

For epoch = 1 to 5:
    For each mini-batch (X_b, y_b) in D_k:
        1. Forward pass:   logits = Model(X_b)
        2. CE Loss:        L_ce = CrossEntropy(logits, y_b)
        3. Proximal term:  L_prox = (mu/2) * SUM( (w_i - w_global_i)^2 )
        4. Total loss:     L = L_ce + L_prox
        5. Backward pass:  Compute gradients
        6. Gradient clip:  Clip grad norm to 1.0
        7. Adam update:    w = w - lr * gradient  [lr=0.001]
Return w_k
""")

doc.add_paragraph()
add_heading('3.4 Weighted Federated Averaging (FedAvg)', 2)
add_code(
"""ALGORITHM: Weighted FedAvg Aggregation
----------------------------------------
INPUT:  Active client set A, weights {w_k}, sample counts {n_k}
OUTPUT: Global model weights w_global

1. N_total = SUM(n_k for k in A)
2. For each layer L:
     w_global[L] = SUM( (n_k / N_total) * w_k[L]  for k in A )
3. Load w_global into server model.

Fault Tolerance: If client k drops out, it is removed from A
and N_total is recalculated over remaining active clients.
""")

doc.add_paragraph()
add_heading('3.5 Local Differential Privacy (LDP)', 2)
add_code(
"""ALGORITHM: Gaussian LDP Noise Injection
-----------------------------------------
INPUT:  Weight tensor w, noise_scale = 0.001
OUTPUT: Privatized weight tensor w_tilde

For each layer tensor w:
    noise   = numpy.random.normal(mean=0, std=noise_scale, size=w.shape)
    w_tilde = w + noise
Return w_tilde

Effect on Accuracy: Less than 0.2% degradation (empirically verified).
""")
doc.add_page_break()

# ── SECTION 4: CORE CODE ───────────────────────────────────────────────────────
add_heading('4. Core Code', 1)

add_heading('4.1 DNA Encryption Engine (DNA_crypto.py)', 2)
add_code(
"""def logistic_map(x0, r, n):
    seq, x = [], x0
    for _ in range(n):
        x = r * x * (1 - x)
        seq.append(x)
    return seq

def encrypt(plaintext, password, rule=1, x0=0.5, r=3.99):
    binary   = text_to_binary(plaintext)
    dna      = binary_to_dna(binary, rule)
    pk       = make_key(password, len(dna))
    ck       = chaotic_to_dna(logistic_map(x0, r, len(dna)))
    combined = dna_xor(pk, ck)
    enc      = dna_xor(dna, combined)
    final    = dna_add(enc, ck)
    return {'cipher': final, 'rule': rule, 'x0': x0, 'r': r}

def decrypt(cipher_dict, password):
    final    = cipher_dict['cipher']
    rule     = cipher_dict['rule']
    x0, r    = cipher_dict['x0'], cipher_dict['r']
    ck       = chaotic_to_dna(logistic_map(x0, r, len(final)))
    enc      = dna_sub(final, ck)
    pk       = make_key(password, len(enc))
    combined = dna_xor(pk, ck)
    dna      = dna_xor(enc, combined)
    return binary_to_text(dna_to_binary(dna, rule))
""")

doc.add_paragraph()
add_heading('4.2 Neural Network Model (FL_Model.py)', 2)
add_code(
"""class CloudSecurityModel(nn.Module):
    def __init__(self, input_size=30, num_classes=2):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, num_classes)
        )   # Total trainable parameters: 4,226

    def forward(self, x):
        return self.network(x)
""")

doc.add_paragraph()
add_heading('4.3 Federated Client (FL_client.py)', 2)
add_code(
"""class FLClient:
    def train_local(self, global_weights=None, epochs=5, mu=0.01):
        self.model.train()
        for epoch in range(epochs):
            for X, y in self.data:
                self.optimizer.zero_grad()
                out  = self.model(X)
                loss = self.criterion(out, y)
                if global_weights is not None:
                    proximal = sum(
                        ((p - g) ** 2).sum()
                        for p, g in zip(self.model.parameters(), global_weights)
                    )
                    loss += (mu / 2) * proximal
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                self.optimizer.step()
        self.scheduler.step()

    def get_weights(self, apply_ldp=True, noise_scale=0.001):
        weights = {}
        for name, param in self.model.state_dict().items():
            w = param.cpu().detach().numpy()
            if apply_ldp:
                w += np.random.normal(0, noise_scale, w.shape)
            weights[name] = w
        return weights
""")

doc.add_paragraph()
add_heading('4.4 FL Server (FL_server.py)', 2)
add_code(
"""class FLServer:
    def aggregate(self, received_weights, sample_counts):
        total = sum(sample_counts.values())
        new_state = {}
        for key in self.global_model.state_dict():
            new_state[key] = sum(
                (sample_counts[cid] / total)
                * torch.tensor(received_weights[cid][key])
                for cid in received_weights
            )
        self.global_model.load_state_dict(new_state)

    def evaluate(self, test_loader):
        self.global_model.eval()
        all_preds, all_labels, all_probs = [], [], []
        with torch.no_grad():
            for X, y in test_loader:
                out   = self.global_model(X)
                probs = torch.softmax(out, dim=1)[:, 1]
                preds = out.argmax(dim=1)
                all_preds.extend(preds.numpy())
                all_labels.extend(y.numpy())
                all_probs.extend(probs.numpy())
        return {
            'accuracy':  accuracy_score(all_labels, all_preds) * 100,
            'f1_score':  f1_score(all_labels, all_preds) * 100,
            'roc_auc':   roc_auc_score(all_labels, all_probs),
        }
""")
doc.add_page_break()

# ── SECTION 5: RESULTS ─────────────────────────────────────────────────────────
add_heading('5. Performance Results', 1)
add_table(
    ['Round', 'Global Accuracy', 'Loss', 'F1-Score', 'ROC-AUC', 'Event'],
    [
        ['1',  '92.86%', '0.3230', '77.89%', '0.9585', 'Client 2 Dropped'],
        ['2',  '96.49%', '0.2719', '88.62%', '0.9786', 'None'],
        ['3',  '98.48%', '0.0634', '94.92%', '0.9850', 'Client 2 Dropped'],
        ['5',  '98.63%', '0.0575', '95.48%', '0.9853', 'Client 1 Dropped'],
        ['8',  '98.84%', '0.0540', '96.16%', '0.9859', 'None'],
        ['13', '98.90%', '0.0528', '96.36%', '0.9860', 'None'],
        ['16', '98.92%', '0.0524', '96.42%', '0.9859', 'None'],
        ['20', '98.88%', '0.0507', '96.29%', '0.9869', 'None'],
    ]
)
doc.add_paragraph()
add_table(
    ['Metric', 'Final Value', 'Industry Benchmark'],
    [
        ['Global Accuracy',         '98.88%',               '>95% (Enterprise Grade)'],
        ['F1-Score',                '96.29%',               '>90% (Conference Grade)'],
        ['ROC-AUC',                 '0.9869',               '>0.98 (Near Perfect)'],
        ['Final Loss',              '0.0507',               '<0.10 (Converged)'],
        ['Fault Tolerance',         '9 dropouts survived',  '100% Stability'],
        ['Cryptographic Integrity', '100% SHA-256 Match',   'Lossless Encryption'],
    ]
)

# ── SAVE ───────────────────────────────────────────────────────────────────────
os.makedirs('results', exist_ok=True)
out = 'results/DNA_FL_Project_Documentation.docx'
try:
    doc.save(out)
    print(f"Saved: {out}")
except PermissionError:
    out_alt = 'results/DNA_FL_Project_Documentation_Standard.docx'
    doc.save(out_alt)
    print(f"File was open in Word. Saved to fallback: {out_alt}")

