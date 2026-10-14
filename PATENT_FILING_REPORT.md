# Patent Filing and Patent-Readiness Report

## DNA-Encrypted Federated Learning Framework

**Prepared for:** Rakul Raj  
**Project repository:** DNA Federated Learning  
**Report date:** 11 October 2026  
**Document status:** Technical and filing-preparation guide; not legal advice

> **Important:** This report is not a patentability opinion and does not replace advice from a
> registered patent agent or patent attorney. Patentability depends on the applicable
> jurisdiction, the full prior-art record, the exact disclosure, inventorship, ownership, and
> claim drafting. Do not file this report unchanged as a patent specification.

## 1. Executive conclusion

The project is a research prototype that combines:

1. Federated training of a cloud-intrusion classification model;
2. client-side model-weight perturbation;
3. a DNA-symbol transformation using `A`, `C`, `G`, and `T`;
4. password-derived and logistic-map-derived sequences;
5. encrypted update exchange with a central server;
6. weighted aggregation and encrypted redistribution of the global model; and
7. a demonstration dashboard and integrity checks.

The broad idea of “using DNA cryptography with federated learning” is unlikely to be a
sufficiently narrow or safe patent position by itself. DNA-inspired cryptography, federated
learning, secure model-update transmission, differential privacy, and chaotic maps are
individually known research areas. A credible patent strategy must identify a specific,
enabled technical improvement that is new over the closest prior art.

The strongest candidate currently visible in this repository is a **computer-implemented
secure model-update transport and reconstruction protocol** with a defined payload format,
per-layer serialization, rule-controlled DNA-symbol conversion, chaotic sequence
combination, authenticated round metadata, validation, and federated aggregation behavior.
The current code does not yet implement all of those production-grade features, so the
candidate should be treated as a **proposed invention direction**, not as an existing
complete invention.

## 2. What is currently implemented

The principal implementation is distributed across:

- [`DNA_crypto.py`](<C:/Users/rakul/Desktop/P%20r%20o%20j%20e%20c%20t%20s/DNA/DNA_crypto.py>): binary/DNA mappings, DNA operations, SHA-256-derived material, logistic-map sequence generation, and tensor serialization;
- [`FL_client.py`](<C:/Users/rakul/Desktop/P%20r%20o%20j%20e%20c%20%20t%20s/DNA/FL_client.py>): local training, proximal regularization, Gaussian noise injection, encryption, and decryption;
- [`FL_server.py`](<C:/Users/rakul/Desktop/P%20r%20o%20j%20e%20c%20%20t%20s/DNA/FL_server.py>): decryption, sample-weighted aggregation, global encryption, and evaluation;
- [`FL_Model.py`](<C:/Users/rakul/Desktop/P%20r%20o%20j%20e%20c%20t%20s/DNA/FL_Model.py>): the PyTorch classifier;
- [`main.py`](<C:/Users/rakul/Desktop/P%20r%20o%20j%20e%20c%20t%20s/DNA/main.py>): synthetic data, experiment orchestration, dropout simulation, metrics, and artifacts;
- [`app.py`](<C:/Users/rakul/Desktop/P%20r%20o%20j%20e%20c%20t%20s/DNA/app.py>): Streamlit dashboard; and
- [`live_demo.py`](<C:/Users/rakul/Desktop/P%20r%20o%20j%20e%20c%20t%20s/DNA/live_demo.py>): terminal demonstration of one training/transfer/aggregation round.

The current live demo shows a complete simulated round:

1. Three local clients are initialized.
2. Each client trains locally.
3. Client 1 encrypts and displays a DNA-symbol payload preview.
4. The server decrypts client payloads.
5. The server performs weighted aggregation.
6. The global model is evaluated.

This is useful evidence of a working prototype, but a demo is not by itself evidence of
novelty, inventive step, security, or patentability.

## 3. Candidate invention concept

### Proposed working title

**A Computer-Implemented Protocol for Protected Federated Model-Update Exchange Using
Layered DNA-Symbol Transformation and Chaotic Sequence Synchronization**

Alternative shorter title:

**DNA-Symbol Protected Federated Learning Model-Update Protocol**

### Technical field

The proposed invention belongs to:

- distributed and federated machine learning;
- secure transmission of machine-learning model updates;
- privacy-preserving computation;
- symbolic sequence transformation; and
- cloud or edge security monitoring.

### Technical problem

In a distributed training system, a client must transmit model updates to an aggregation
server without transmitting raw training records. Plaintext updates can reveal information
about local data, while a transport scheme that does not preserve tensor metadata can cause
incorrect reconstruction or model corruption. Client heterogeneity, intermittent
connectivity, and repeated update rounds add further protocol problems.

The proposed system should therefore address a concrete technical problem:

> How can a federated-learning client package model-layer updates into a validated,
> reconstructible protected payload that preserves tensor metadata, supports heterogeneous
> client participation, and allows the server to aggregate only valid updates?

### Proposed technical solution

A strengthened implementation would:

1. train a local model without transmitting raw data;
2. clip and optionally privatize an update;
3. serialize every model layer with its name, dtype, shape, round number, and client identity;
4. convert the serialized bytes into two-bit symbols;
5. select a reversible symbol mapping from a rule identifier;
6. generate a synchronized chaotic sequence from a protected parameter set;
7. combine password/key-derived and chaotic sequences;
8. apply a reversible layered symbol transformation;
9. authenticate the complete payload and associated metadata;
10. reject invalid, replayed, duplicate, malformed, or out-of-round payloads;
11. decrypt and reconstruct valid layer tensors; and
12. perform sample-weighted aggregation only over accepted client updates.

The last five steps are particularly important. They convert a visual DNA-encoding
demonstration into a concrete communications and model-update protocol that can be tested
for technical effects.

## 4. Patentability assessment

### Novelty

Novelty asks whether one earlier reference discloses every element of the claimed invention.
The repository alone cannot answer this. A professional prior-art search is required for:

- DNA cryptography and nucleotide-symbol encryption;
- chaotic-map cryptography;
- encrypted federated-learning updates;
- secure aggregation;
- privacy-preserving model updates;
- model-update serialization and validation; and
- intrusion detection using federated learning.

Do not assume that a combination is novel merely because the exact project title has not been
found.

### Inventive step / non-obviousness

An examiner may argue that a skilled person could combine known DNA encoding, chaotic maps,
federated learning, and Gaussian noise. The application must therefore show a non-obvious
technical arrangement and a measurable technical effect, for example:

- lower update reconstruction failure under heterogeneous tensor shapes;
- reduced invalid-update processing;
- lower communication overhead than a defined baseline;
- improved tamper/replay rejection;
- deterministic, interoperable reconstruction across clients;
- reduced server processing cost; or
- improved convergence under a measured client-dropout condition.

Accuracy alone is usually weak evidence for a cryptographic transport invention.

### Enablement and support

The specification must describe enough detail for a skilled person to implement the claimed
protocol. It should include:

- payload fields and byte/character encoding;
- mapping-rule selection;
- key and chaotic-sequence derivation;
- reversible operations and their inverse order;
- tensor shape/dtype handling;
- authentication and replay checks;
- aggregation acceptance rules;
- error handling;
- parameter ranges; and
- experimental results.

Avoid claiming an unspecified “quantum-resistant” result. If post-quantum security is part of
the invention, obtain cryptographic review and compare against recognized post-quantum
constructions. DNA symbols and a chaotic map do not, by themselves, establish post-quantum
security.

### Patent-eligibility for software

For software-related inventions, the application should be framed around a concrete
technical system and technical effect rather than an abstract algorithm, business method, or
generic use of a computer. In India, computer-related inventions are subject to Section 3(k)
of the Patents Act; current examination guidance emphasizes the substance of the claim and
whether the implementation produces a technical effect or technical contribution. The
position must be checked against the current official guidance and the advice of an Indian
patent professional when filing.

## 5. What should be changed before filing

### Required technical improvements

The current prototype should be strengthened before relying on it as patent evidence:

1. **Add authenticated payloads.** Use a recognized authenticated-encryption or MAC design
   for the actual security layer. Keep the DNA transform as the experimental symbol layer.
2. **Add explicit payload metadata.** Include protocol version, client ID, round number,
   model version, layer names, dtype, shape, nonce, authentication tag, and timestamp.
3. **Add validation.** Reject unknown clients, invalid symbols, invalid shapes, unsupported
   dtypes, stale rounds, duplicate updates, and altered payloads.
4. **Add replay protection.** Bind the authenticated payload to a unique round and update ID.
5. **Separate key management from passwords.** Use a key-derivation scheme, rotation, and
   secret storage; remove credentials from source code.
6. **Define formal privacy.** If privacy is claimed, add clipping, calibrated noise, and
   epsilon/delta accounting. Otherwise describe the feature as noise injection.
7. **Create an experiment harness.** Record configuration, seed, dataset version, payload
   size, encryption time, decryption time, rejection count, aggregation time, and metrics.
8. **Add baselines.** Compare plaintext FedAvg, FedProx, standard authenticated encryption,
   the DNA layer, and combinations.
9. **Add repeatable tests.** Test round-trip reconstruction, tamper rejection, replay
   rejection, malformed payload handling, dropout, and aggregation.
10. **Create a versioned invention branch/tag.** Preserve the exact source, diagrams,
    datasets, configuration, and results that support the filing.

### Claims should not rely on unsupported statements

Avoid unqualified claims such as:

- “100% secure”;
- “guaranteed quantum-resistant”;
- “zero inversion risk”;
- “formal differential privacy” without accounting; or
- “real AWS/Azure/GCP deployment” when the nodes are simulated locally.

These statements can create enablement, clarity, credibility, and examination problems.

## 6. Suggested claim architecture

These are claim-design directions for a patent professional, not final legal claims.

### Independent system claim direction

A distributed model-update protection system comprising:

1. a plurality of client computing devices configured to train local model instances on
   respective private datasets;
2. a client-side serializer configured to generate layer records containing model-layer
   identifiers and reconstruction metadata;
3. a symbol encoder configured to convert serialized update data into nucleotide symbols
   according to a selected reversible mapping rule;
4. a sequence generator configured to generate a synchronized transformation sequence;
5. a layered symbol-transform module configured to produce a protected update payload;
6. a payload-authentication module configured to bind the payload to a client and training
   round;
7. an aggregation server configured to validate and reconstruct accepted payloads; and
8. an aggregation module configured to calculate a sample-weighted global model from valid
   reconstructed updates and distribute a protected global update.

### Independent method claim direction

A computer-implemented method comprising:

1. locally training a model;
2. generating a protected update without transmitting local training records;
3. serializing model-layer values and reconstruction metadata;
4. applying a reversible nucleotide-symbol transformation controlled by a mapping rule and
   synchronized sequence;
5. authenticating the resulting payload with round-bound metadata;
6. transmitting the payload to an aggregation server;
7. validating the payload and rejecting invalid, stale, duplicate, or unauthenticated
   payloads;
8. reconstructing valid model-layer tensors; and
9. performing weighted federated aggregation using the valid tensors.

### Dependent-claim subjects

Potential dependent claims may cover:

- eight or more mapping rules;
- a logistic-map or other specified sequence generator;
- per-layer rather than whole-model serialization;
- dtype and shape preservation;
- Gaussian noise after clipping;
- client dropout and minimum-participation rules;
- payload versioning;
- replay protection;
- checksum or authenticated-integrity verification;
- adaptive mapping selection based on client or round state;
- payload-size or processing-time improvements demonstrated by experiments; and
- encrypted redistribution of the global model.

The final claims must be drafted only after the prior-art search and after the implementation
supports every claimed limitation.

## 7. Documents and evidence to prepare

Create an invention disclosure package containing:

### Technical documents

- one-page invention summary;
- detailed system architecture;
- protocol sequence diagram;
- client-to-server message format;
- encryption/transformation flow;
- decryption/reconstruction flow;
- aggregation and rejection flow;
- threat model;
- parameter table;
- pseudocode;
- implementation notes;
- test plan; and
- baseline and ablation results.

### Evidence documents

- dated source archive or Git tag;
- commit history;
- experiment configuration files;
- raw metric outputs;
- test results;
- screenshots of the working demo;
- authorship/inventorship records;
- names of all contributors and what each contributed;
- employer, university, sponsor, or grant agreements; and
- records of any public presentation, GitHub publication, paper, poster, video, or social-media
  disclosure.

Do not include real passwords, private keys, personal data, or confidential cloud credentials
in the evidence archive.

## 8. Filing strategy

### Step 1: Stop avoidable public disclosure

Before a patent filing, avoid publishing new implementation details, claims, diagrams,
benchmarks, or source code that reveal the proposed inventive features. Your repository and
existing documents may already be public, so immediately record their publication dates and
ask counsel to assess their effect on novelty and grace-period rules.

### Step 2: Confirm inventors and ownership

Inventors are the people who contributed to the conception of the claimed invention, not
every person who wrote code or supervised the project. Ownership may belong to an employer,
university, sponsor, or company under an agreement. Resolve this before filing.

### Step 3: Run a professional prior-art search

Search patent and non-patent literature using combinations of:

- DNA cryptography;
- nucleotide encoding encryption;
- chaotic-map encryption;
- federated learning encrypted gradients;
- secure aggregation;
- privacy-preserving model updates;
- distributed intrusion detection;
- model update serialization; and
- authenticated federated protocols.

Use the results to narrow the claims around the genuinely new technical arrangement.

### Step 4: Choose an initial filing

Common options are:

- **Provisional application:** establishes an early filing date while development continues;
  the later complete specification must fully support the claimed invention.
- **Complete application:** suitable when the invention, embodiments, and claims are mature.
- **International/PCT route:** generally considered after an initial filing when protection in
  multiple countries is needed. A priority claim generally depends on filing within the
  applicable 12-month priority period.

The correct route depends on the applicant's residence, ownership, disclosure history,
commercial plans, budget, and target countries.

### Step 5: Draft and file with a patent professional

The filing package normally includes:

- applicant and inventor information;
- title;
- abstract;
- background;
- summary;
- detailed description;
- drawings;
- claims for a complete application;
- priority information, if applicable;
- required forms and declarations; and
- official filing fees.

Use the official patent office portal and current forms. Filing fees and procedural
requirements change, so verify them immediately before submission.

### Step 6: Maintain the application

After filing, track:

- priority deadlines;
- complete-specification deadlines;
- examination requests;
- office actions;
- response deadlines;
- assignment and inventor declarations;
- publication;
- renewal/annuity fees; and
- foreign-filing decisions.

Do not rely on a provisional filing as a substitute for a complete, enabling disclosure.

## 9. India-focused route

If India is the first filing country, discuss the following with a registered Indian patent
agent:

1. Whether the claims demonstrate a technical effect or technical contribution beyond a
   computer program or algorithm per se.
2. Whether a provisional or complete specification is appropriate.
3. The current requirements for application and specification forms.
4. Applicant category, fee status, inventor declarations, and assignment documents.
5. Whether a prior public GitHub or presentation disclosure affects novelty or any available
   grace-period argument.
6. Foreign-filing permission or other restrictions if an overseas filing will follow.
7. Examination-request timing and responses to objections under the current rules.

The official Indian Patent Office/CGPDTM website and e-filing portal should be used for the
current forms, fees, and procedural instructions:

- https://ipindia.gov.in/
- https://ipronline.ipindia.gov.in/

Because this project is software-heavy, the patent agent should specifically review the
current Computer Related Inventions guidance and frame the invention around the secure
distributed-computing technical effect, not merely the abstract mathematical operations.

## 10. International route

If protection outside India is important, discuss a priority filing followed by national
filings or a PCT application. WIPO describes the PCT as an international filing route; it
does not itself grant a worldwide patent. National or regional offices ultimately examine and
grant rights.

The usual priority planning principle is to make the international filing decision within
12 months of the earliest priority filing, subject to the applicable rules and professional
advice:

- https://www.wipo.int/en/web/pct-system/filing/index

For the United States, a provisional application is commonly followed by a corresponding
nonprovisional application within the applicable 12-month period:

- https://www.uspto.gov/patents/basics/using-legal-services/provisional-application

Confirm all deadlines and restoration rules directly with the relevant office or patent
professional.

## 11. Suggested patent abstract draft

> A computer-implemented system protects federated machine-learning model updates exchanged
> between client devices and an aggregation server. Each client trains a local model without
> transmitting local training records, serializes model-layer values together with layer
> reconstruction metadata and training-round metadata, and converts the serialized update
> into nucleotide symbols according to a reversible mapping rule. A synchronized sequence is
> generated using protected transformation parameters and combined with key-derived sequence
> material to produce a layered symbol-transformed update payload. The payload is
> authenticated and transmitted to the aggregation server. The server validates client,
> round, integrity, and reconstruction information, rejects invalid or replayed payloads,
> reconstructs valid model-layer tensors, and performs sample-weighted federated aggregation.
> A protected global model update is then generated and distributed to participating clients.

This abstract should be revised after the implementation, prior-art search, and claim scope
are settled.

## 12. Immediate 30-day action plan

### Days 1–5: invention control

- Freeze the current version in a private archive.
- Record repository and document publication dates.
- List every contributor.
- Identify employer, university, sponsor, or grant ownership obligations.
- Stop new public disclosure of the proposed improvements.

### Days 6–12: technical strengthening

- Implement payload metadata and versioning.
- Add authentication and replay protection.
- Add input validation and rejection logging.
- Remove hard-coded credentials.
- Add round-trip, tamper, replay, and malformed-payload tests.

### Days 13–20: experimental evidence

- Run plaintext FedAvg, FedProx, DNA layer, and authenticated baseline experiments.
- Measure accuracy, F1, ROC-AUC, convergence, payload size, encryption time, decryption time,
  aggregation time, rejected updates, and dropout behavior.
- Repeat experiments with multiple seeds.

### Days 21–30: patent preparation

- Commission a professional prior-art search.
- Prepare invention disclosure and drawings.
- Review inventorship and ownership.
- Ask a registered patent agent to draft and file the appropriate application.
- Calendar the priority and complete-specification deadlines.

## 13. Final recommendation

Do not file a broad application claiming “DNA cryptography combined with federated
learning.” Instead, develop and document a specific protocol whose technical effect can be
measured:

> validated, authenticated, round-bound, layer-preserving protected model-update transport
> for federated aggregation under heterogeneous and unreliable client participation.

That direction is narrower, more technically defensible, and better aligned with the actual
software architecture. A patent professional should still confirm whether the final
implementation is new and non-obvious after a complete prior-art search.

## Sources and further reading

- Indian Patent Office/CGPDTM: https://ipindia.gov.in/
- Indian patent e-filing portal: https://ipronline.ipindia.gov.in/
- WIPO PCT filing information: https://www.wipo.int/en/web/pct-system/filing/index
- USPTO provisional application information:
  https://www.uspto.gov/patents/basics/using-legal-services/provisional-application
- Project implementation: [`DNA_crypto.py`](<C:/Users/rakul/Desktop/P%20r%20o%20j%20e%20c%20t%20s/DNA/DNA_crypto.py>),
  [`FL_client.py`](<C:/Users/rakul/Desktop/P%20r%20o%20j%20e%20c%20t%20s/DNA/FL_client.py>),
  [`FL_server.py`](<C:/Users/rakul/Desktop/P%20r%20o%20j%20c%20t%20s/DNA/FL_server.py>),
  and [`live_demo.py`](<C:/Users/rakul/Desktop/P%20r%20o%20j%20c%20t%20s/DNA/live_demo.py>)
