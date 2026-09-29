import streamlit as st
import time
import torch
import pandas as pd
import numpy as np
import os
import random
import hashlib
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from sklearn.metrics import confusion_matrix
import seaborn as sns
from main import prepare_data
from FL_Model import CloudSecurityModel
from FL_client import FLClient
from FL_server import FLServer
from DNA_crypto import encrypt_weights, decrypt_weights, encrypt, decrypt

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="DNA-FL Security Dashboard", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    .big-font {font-size:20px !important; font-weight: bold;}
    .dna-font {font-family: 'Courier New', monospace; color: #2ecc71; word-wrap: break-word; font-size:12px;}
    .intrusion {background-color: rgba(231,76,60,0.2); border-left:5px solid #e74c3c; padding:10px; border-radius:4px; margin-bottom:5px;}
    .normal    {background-color: rgba(46,204,113,0.1); border-left:5px solid #2ecc71; padding:10px; border-radius:4px; margin-bottom:5px;}
    .ok-badge  {background-color:#2ecc71; color:white; padding:2px 8px; border-radius:4px; font-size:12px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🧬 DNA-Encrypted Federated Learning Framework")
st.markdown("**Quantum-Resistant Multi-Cloud Data Security Architecture**")

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Simulation Settings")
num_rounds   = st.sidebar.slider("Federated Rounds",        min_value=1, max_value=20, value=5)
local_epochs = st.sidebar.slider("Local Epochs per Round",  min_value=1, max_value=5,  value=2)
st.sidebar.markdown("---")
st.sidebar.info("Decentralized FL where model weights are secured via DNA cryptography (XOR/ADD + Chaotic Maps).")

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "🚀 Phase 1: Federated Training",
    "🛡️ Phase 2: Live Threat Detection",
    "🔐 Phase 3: Cryptographic Verification"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — FEDERATED TRAINING
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    if st.button("🚀 Start Live Simulation", type="primary"):

        clients_data, test_loader, input_size = prepare_data(num_clients=3)

        global_model = CloudSecurityModel(input_size)
        server       = FLServer(global_model, password="ServerSecretKey2024")

        clients, names = [], ["AWS Node", "Azure Node", "GCP Node"]
        for i in range(3):
            clients.append(FLClient(
                i+1, clients_data[i], CloudSecurityModel(input_size),
                f"Client{i+1}@SecurePass2024", "ServerSecretKey2024"
            ))

        st.success("✅ Connected to AWS, Azure, and GCP Nodes successfully.")

        # ── placeholders ──────────────────────────────────────────────────────
        progress_bar = st.progress(0)
        round_text   = st.empty()

        c1, c2, c3   = st.columns(3)
        status_boxes = [c1.empty(), c2.empty(), c3.empty()]

        st.markdown("### 🔐 Intercepted Network Traffic (DNA Encryption Preview)")
        network_box = st.empty()

        # ── FEATURE 2: per-client + global accuracy chart ─────────────────────
        st.markdown("### 📊 Per-Client vs Global Accuracy")
        client_chart = st.empty()

        st.markdown("### 📈 Global Convergence")
        gcol1, gcol2 = st.columns(2)
        acc_chart  = gcol1.empty()
        loss_chart = gcol2.empty()

        # ── FEATURE 3: encryption overhead chart ─────────────────────────────
        st.markdown("### ⏱️ Encryption Overhead vs Accuracy Trade-off")
        overhead_chart = st.empty()

        metric_cols = st.columns(4)
        m1 = metric_cols[0].empty()
        m2 = metric_cols[1].empty()
        m3 = metric_cols[2].empty()
        m4 = metric_cols[3].empty()

        # ── history storage ───────────────────────────────────────────────────
        global_acc_hist, global_loss_hist = [], []
        client_acc_hist = {i: [] for i in range(3)}   # per-client per round
        enc_time_hist   = []                           # avg encrypt time per round

        # ── federated loop ────────────────────────────────────────────────────
        for rnd in range(1, num_rounds + 1):
            round_text.markdown(
                f"<p class='big-font'>🔄 Federated Round {rnd} / {num_rounds}</p>",
                unsafe_allow_html=True)
            progress_bar.progress(rnd / num_rounds)

            # local training
            for idx, c in enumerate(clients):
                status_boxes[idx].info(f"**{names[idx]}**\n\n⚙️ Training on Intrusion Logs...")

            round_enc_times = []
            for idx, c in enumerate(clients):
                global_weights_tensors = list(server.model.parameters())
                loss, acc = c.train_local(global_weights=global_weights_tensors, epochs=local_epochs)
                client_acc_hist[idx].append(acc)
                status_boxes[idx].success(
                    f"**{names[idx]}**\n\n✅ Done\n\nLocal Acc: {acc:.2f}%")

            time.sleep(0.3)

            # encryption & transmission
            active_clients = []
            for idx, c in enumerate(clients):
                status_boxes[idx].warning(
                    f"**{names[idx]}**\n\n🧬 Encrypting to DNA...")

                if random.random() < 0.1:
                    status_boxes[idx].error(
                        f"**{names[idx]}**\n\n❌ Connection Lost")
                    continue

                enc_payload = c.encrypt_and_send()
                round_enc_times.append(
                    c.encrypt_times[-1] * 1000 if c.encrypt_times else 0)

                server.receive_update(c.id, enc_payload, c.password, c.num_samples)
                active_clients.append(c)

                if len(active_clients) == 1:
                    fk         = list(enc_payload.keys())[0]
                    dna_cipher = enc_payload[fk]['cipher']
                    payload_mb = sum(
                        len(v['cipher']) for v in enc_payload.values()) / 1024 / 1024
                    network_box.markdown(f"""
                    <div style='background:#0e1117;padding:10px;border-radius:5px;border:1px solid #2ecc71;'>
                    <p style='color:#2ecc71;margin-bottom:0;'>
                    <strong>[PACKET INTERCEPTED] Source: {names[idx]} | Payload: {payload_mb:.2f} MB</strong></p>
                    <p class='dna-font'>{dna_cipher[:220]}… [TRUNCATED]</p>
                    </div>""", unsafe_allow_html=True)

                status_boxes[idx].success(
                    f"**{names[idx]}**\n\n🚀 Transmitted securely.")

            time.sleep(0.5)

            # aggregation
            server.aggregate()
            enc_global = server.encrypt_global()
            for c in active_clients:
                c.receive_and_decrypt(enc_global)

            # evaluation
            metrics = server.evaluate(test_loader)
            global_acc_hist.append(metrics['accuracy'])
            global_loss_hist.append(metrics['loss'])
            enc_time_hist.append(
                np.mean(round_enc_times) if round_enc_times else 0)

            rounds_idx = list(range(1, rnd + 1))

            # ── FEATURE 2: per-client accuracy chart ─────────────────────────
            fig2, ax2 = plt.subplots(figsize=(8, 3))
            for idx, cname in enumerate(names):
                ax2.plot(rounds_idx, client_acc_hist[idx],
                         marker='o', label=cname, linestyle='--', alpha=0.7)
            ax2.plot(rounds_idx, global_acc_hist,
                     marker='s', label='Global Model', linewidth=2.5, color='white')
            ax2.set_xlabel("Round"); ax2.set_ylabel("Accuracy (%)")
            ax2.legend(); ax2.set_facecolor('#0e1117')
            fig2.patch.set_facecolor('#0e1117')
            ax2.tick_params(colors='white'); ax2.xaxis.label.set_color('white')
            ax2.yaxis.label.set_color('white')
            for spine in ax2.spines.values(): spine.set_edgecolor('#444')
            client_chart.pyplot(fig2)
            plt.close(fig2)

            # global charts
            df = pd.DataFrame(
                {'Accuracy': global_acc_hist, 'Loss': global_loss_hist},
                index=rounds_idx)
            acc_chart.line_chart(df['Accuracy'],  color="#2ecc71")
            loss_chart.line_chart(df['Loss'],     color="#e74c3c")

            # ── FEATURE 3: encryption overhead chart ─────────────────────────
            fig3, ax3a = plt.subplots(figsize=(8, 3))
            ax3b = ax3a.twinx()
            ax3a.bar(rounds_idx, enc_time_hist,
                     color='#3498db', alpha=0.6, label='Enc Time (ms)')
            ax3b.plot(rounds_idx, global_acc_hist,
                      color='#2ecc71', marker='o', label='Global Acc (%)')
            ax3a.set_xlabel("Round")
            ax3a.set_ylabel("Avg Encrypt Time (ms)", color='#3498db')
            ax3b.set_ylabel("Global Accuracy (%)",   color='#2ecc71')
            ax3a.set_facecolor('#0e1117')
            fig3.patch.set_facecolor('#0e1117')
            ax3a.tick_params(colors='white')
            ax3b.tick_params(colors='white')
            lines1, lab1 = ax3a.get_legend_handles_labels()
            lines2, lab2 = ax3b.get_legend_handles_labels()
            ax3a.legend(lines1 + lines2, lab1 + lab2, loc='lower right')
            for spine in ax3a.spines.values(): spine.set_edgecolor('#444')
            overhead_chart.pyplot(fig3)
            plt.close(fig3)

            # metrics row
            prev_acc  = global_acc_hist[-2]  if rnd > 1 else metrics['accuracy']
            prev_loss = global_loss_hist[-2] if rnd > 1 else metrics['loss']
            m1.metric("Global Accuracy", f"{metrics['accuracy']:.2f}%",
                      f"{metrics['accuracy']-prev_acc:+.2f}%")
            m2.metric("Loss",            f"{metrics['loss']:.4f}",
                      f"{metrics['loss']-prev_loss:+.4f}", delta_color="inverse")
            m3.metric("F1-Score",  f"{metrics['f1_score']:.2f}%")
            m4.metric("ROC-AUC",   f"{metrics['roc_auc']:.4f}")

        # ── FEATURE 1: Confusion Matrix ───────────────────────────────────────
        st.markdown("### 🔢 Final Confusion Matrix")
        global_model.eval()
        all_preds, all_labels = [], []
        with torch.no_grad():
            for data, target in test_loader:
                preds = global_model(data).argmax(dim=1).numpy()
                all_preds.extend(preds)
                all_labels.extend(target.numpy())

        cm = confusion_matrix(all_labels, all_preds)
        fig_cm, ax_cm = plt.subplots(figsize=(5, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
                    xticklabels=["Normal", "Intrusion"],
                    yticklabels=["Normal", "Intrusion"],
                    ax=ax_cm, linewidths=0.5)
        ax_cm.set_xlabel("Predicted"); ax_cm.set_ylabel("Actual")
        ax_cm.set_title("Global Model — Confusion Matrix")
        fig_cm.patch.set_facecolor('#0e1117')
        ax_cm.set_facecolor('#0e1117')
        ax_cm.tick_params(colors='white')
        ax_cm.xaxis.label.set_color('white')
        ax_cm.yaxis.label.set_color('white')
        ax_cm.title.set_color('white')
        st.pyplot(fig_cm)
        plt.close(fig_cm)

        tn, fp, fn, tp = cm.ravel()
        st.markdown(f"""
        | Metric | Value |
        |--------|-------|
        | True Positive (Intrusions correctly caught) | **{tp}** |
        | True Negative (Normal traffic correctly passed) | **{tn}** |
        | False Positive (Normal flagged as threat) | **{fp}** |
        | False Negative (Missed intrusions) | **{fn}** |
        """)

        # save model
        os.makedirs("results", exist_ok=True)
        model_path = "results/secure_global_model.pth"
        torch.save(global_model.state_dict(), model_path)
        st.success("✅ Training Complete — Global Model Converged")
        with open(model_path, "rb") as f:
            st.download_button("💾 Download Trained Global Model (.pth)",
                               f, "secure_global_model.pth",
                               mime="application/octet-stream")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — LIVE THREAT DETECTION  (FEATURE 4: Manual Packet Injection)
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 🛡️ Real-Time Threat Detection")

    if not os.path.exists("results/secure_global_model.pth"):
        st.warning("⚠️ Run Phase 1 first to train the model.")
    else:
        st.markdown("#### Option A — Intercept Random Network Traffic")
        if st.button("📡 Intercept & Analyze 10 Random Packets", type="primary"):
            model = CloudSecurityModel(input_size=30)
            model.load_state_dict(torch.load("results/secure_global_model.pth",
                                             weights_only=False))
            model.eval()

            features = np.random.randn(10, 30)
            features[2] += 2.8; features[7] += 3.2   # inject 2 malicious

            tensor_f = torch.FloatTensor(features)
            with torch.no_grad():
                outputs = model(tensor_f)
                probs   = torch.softmax(outputs, dim=1)[:, 1].numpy()
                preds   = outputs.argmax(dim=1).numpy()

            threat_types = ["DDoS", "Port Scan", "Brute Force",
                            "SQL Injection", "Man-in-the-Middle"]
            for i in range(10):
                ip   = f"192.168.{random.randint(0,255)}.{random.randint(2,254)}"
                port = random.randint(1024, 65535)
                size = random.randint(64, 1500)
                ts   = time.strftime("%H:%M:%S")
                time.sleep(0.3)
                if preds[i] == 1:
                    threat = random.choice(threat_types)
                    st.markdown(
                        f"<div class='intrusion'>🚨 <strong>[{ts}] INTRUSION BLOCKED</strong> "
                        f"— Type: {threat} | IP: {ip}:{port} | "
                        f"Size: {size}B | Confidence: {probs[i]*100:.1f}%</div>",
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        f"<div class='normal'>✅ <strong>[{ts}] NORMAL TRAFFIC</strong>"
                        f" — IP: {ip}:{port} | Size: {size}B | "
                        f"Confidence: {(1-probs[i])*100:.1f}%</div>",
                        unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### Option B — Manual Packet Injection")
        st.markdown("Manually craft a network packet and let the model classify it in real-time.")

        with st.expander("🔧 Adjust Packet Parameters"):
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                packet_size       = st.slider("Packet Size (bytes)",  64, 65535, 512)
                failed_logins     = st.slider("Failed Login Attempts", 0, 50, 0)
                tcp_flags         = st.slider("TCP Flag Value",        0, 255, 2)
                connection_rate   = st.slider("Connection Rate (conn/s)", 0, 500, 10)
            with col_b:
                port_scan_count   = st.slider("Port Scan Count",       0, 1000, 0)
                data_exfil_rate   = st.slider("Data Exfil Rate (KB/s)",0, 1000, 5)
                ttl_value         = st.slider("TTL Value",             0, 255, 64)
                protocol_anomaly  = st.slider("Protocol Anomaly Score",0.0, 1.0, 0.0)
            with col_c:
                src_entropy       = st.slider("Source IP Entropy",     0.0, 8.0, 3.5)
                duration          = st.slider("Connection Duration (s)",0, 3600, 30)

        if st.button("🔍 Classify This Packet", type="secondary"):
            model = CloudSecurityModel(input_size=30)
            model.load_state_dict(torch.load("results/secure_global_model.pth",
                                             weights_only=False))
            model.eval()

            # Build 30-feature vector from the manual inputs
            manual_inputs = [
                packet_size / 65535, failed_logins / 50, tcp_flags / 255,
                connection_rate / 500, port_scan_count / 1000,
                data_exfil_rate / 1000, ttl_value / 255,
                protocol_anomaly, src_entropy / 8.0, duration / 3600
            ]
            # Pad remaining 20 features with random noise (latent features)
            manual_inputs += list(np.random.randn(20) * 0.1)

            tensor_f = torch.FloatTensor([manual_inputs])
            with torch.no_grad():
                output = model(tensor_f)
                prob   = torch.softmax(output, dim=1)[0][1].item()
                pred   = output.argmax(dim=1).item()

            if pred == 1:
                st.error(
                    f"🚨 **INTRUSION DETECTED** — Threat Confidence: {prob*100:.1f}%\n\n"
                    "Action: Packet blocked. IP flagged for investigation.")
            else:
                st.success(
                    f"✅ **NORMAL TRAFFIC** — Safe Confidence: {(1-prob)*100:.1f}%\n\n"
                    "Action: Packet forwarded to destination.")

            st.progress(prob, text=f"Threat Probability: {prob*100:.1f}%")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CRYPTOGRAPHIC VERIFICATION  (FEATURE 5: SHA-256 Integrity Check)
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 🔐 Cryptographic Integrity Verification")
    st.markdown(
        "This panel proves that DNA encryption is **lossless** — "
        "model weights are byte-identical after encryption and decryption.")

    if st.button("🧪 Run Integrity Verification", type="primary"):
        st.info("Generating a test model, encrypting weights, decrypting, and comparing SHA-256 checksums...")

        # Create a fresh model and extract weights
        test_model   = CloudSecurityModel(input_size=30)
        password     = "ServerSecretKey2024"
        rule, x0, r = 2, 0.35, 3.99

        original_weights = {
            name: param.cpu().detach().numpy()
            for name, param in test_model.state_dict().items()
        }

        # SHA-256 of original weights
        original_hashes = {}
        for name, w in original_weights.items():
            h = hashlib.sha256(w.tobytes()).hexdigest()
            original_hashes[name] = h

        # Encrypt
        with st.spinner("🧬 Encrypting weights to DNA sequences..."):
            t0          = time.time()
            encrypted   = encrypt_weights(original_weights, password, rule, x0, r)
            enc_time    = (time.time() - t0) * 1000

        # Decrypt
        with st.spinner("🔓 Decrypting DNA sequences back to weights..."):
            t1          = time.time()
            decrypted   = decrypt_weights(encrypted, password)
            dec_time    = (time.time() - t1) * 1000

        # SHA-256 of decrypted weights
        decrypted_hashes = {}
        for name, w in decrypted.items():
            h = hashlib.sha256(w.tobytes()).hexdigest()
            decrypted_hashes[name] = h

        # Show comparison
        st.markdown("#### Checksum Comparison (SHA-256)")
        all_match = True
        rows = []
        for name in original_hashes:
            match     = original_hashes[name] == decrypted_hashes[name]
            all_match = all_match and match
            rows.append({
                "Layer":              name,
                "Original SHA-256":   original_hashes[name][:20] + "...",
                "Decrypted SHA-256":  decrypted_hashes[name][:20] + "...",
                "Status":             "✅ MATCH" if match else "❌ MISMATCH"
            })

        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        if all_match:
            st.success(
                f"✅ **INTEGRITY VERIFIED** — All {len(rows)} weight tensors "
                f"match perfectly after DNA encrypt/decrypt.\n\n"
                f"Encryption: **{enc_time:.1f} ms** | "
                f"Decryption: **{dec_time:.1f} ms**")
        else:
            st.error("❌ Integrity check failed — data corruption detected.")

        # Show one full DNA payload as proof
        fk = list(encrypted.keys())[0]
        dna_sample = encrypted[fk]['cipher']
        dna_size   = len(dna_sample)
        st.markdown(f"#### Sample DNA Cipher (Layer: `{fk}`, Length: {dna_size:,} bases)")
        st.markdown(f"""
        <div style='background:#0e1117;padding:12px;border-radius:5px;border:1px solid #2ecc71;'>
        <p class='dna-font'>{dna_sample[:300]}…</p>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        | Property | Value |
        |----------|-------|
        | DNA Bases Used | A, C, G, T |
        | Chaotic Map | Logistic Map (x₀={x0}, r={r}) |
        | Encoding Rule | Rule {rule} |
        | Cipher Length | {dna_size:,} bases |
        | Encryption Time | {enc_time:.1f} ms |
        | Decryption Time | {dec_time:.1f} ms |
        """)

    st.markdown("---")
    st.markdown("#### 🧬 Live DNA Text Encryptor & Decryptor Sandbox")
    st.markdown("Type any secret text, telemetry record, or key to test biological DNA encryption live.")

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        input_text = st.text_area("Secret Message / Telemetry Data", "CONFIDENTIAL: Patient Record #4092 - Heart Rate High", height=100)
        secret_pass = st.text_input("Encryption Password / Key", "SecretPass2026")
    with col_t2:
        dna_rule = st.selectbox("DNA Encoding Rule (1-8)", options=list(range(1, 9)), index=1)
        x0_param = st.slider("Chaotic Map Seed (x₀)", 0.1, 0.9, 0.35)
        r_param = st.slider("Chaotic Parameter (r)", 3.57, 4.0, 3.99)

    if st.button("🔒 Encrypt Message to DNA Sequence", type="secondary"):
        if input_text:
            cipher_res = encrypt(input_text, secret_pass, rule=dna_rule, x0=x0_param, r=r_param)
            st.session_state['dna_cipher_demo'] = cipher_res
            st.session_state['dna_pass_demo'] = secret_pass
            st.success("✅ Encrypted Successfully!")
            
            dna_str = cipher_res['cipher']
            st.markdown(f"**Ciphertext Length:** {len(dna_str)} bases")
            st.markdown(f"""
            <div style='background:#0e1117;padding:12px;border-radius:5px;border:1px solid #2ecc71;'>
            <p style='color:#2ecc71;margin-bottom:4px;'><strong>🧬 Biological DNA Sequence Payload:</strong></p>
            <p class='dna-font'>{dna_str}</p>
            </div>""", unsafe_allow_html=True)

    if 'dna_cipher_demo' in st.session_state:
        st.markdown("##### Decryption Test")
        decrypt_pass = st.text_input("Enter Password to Decrypt", st.session_state['dna_pass_demo'], key="dec_pass_input")
        if st.button("🔓 Decrypt DNA Sequence Back to Text"):
            try:
                decrypted_msg = decrypt(st.session_state['dna_cipher_demo'], decrypt_pass)
                if decrypted_msg:
                    st.success(f"✅ **Decrypted Output:** `{decrypted_msg}`")
                else:
                    st.error("❌ Decryption failed or incorrect password.")
            except Exception as e:
                st.error(f"❌ Decryption Failed: {str(e)}")

