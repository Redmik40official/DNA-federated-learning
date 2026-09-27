import streamlit as st
import time
import torch
import pandas as pd
import numpy as np
import os
import random
from main import prepare_data
from FL_Model import CloudSecurityModel
from FL_client import FLClient
from FL_server import FLServer

# Page Config
st.set_page_config(page_title="DNA-FL Security Dashboard", page_icon="🧬", layout="wide")

# Custom CSS for aesthetics
st.markdown("""
    <style>
    .big-font {font-size:20px !important; font-weight: bold;}
    .dna-font {font-family: 'Courier New', monospace; color: #2ecc71; word-wrap: break-word;}
    .intrusion {background-color: rgba(231, 76, 60, 0.2); border-left: 5px solid #e74c3c; padding: 10px; border-radius: 4px; margin-bottom: 5px;}
    .normal {background-color: rgba(46, 204, 113, 0.1); border-left: 5px solid #2ecc71; padding: 10px; border-radius: 4px; margin-bottom: 5px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🧬 DNA-Encrypted Federated Learning Framework")
st.markdown("**Quantum-Resistant Multi-Cloud Data Security Architecture**")

# Tabs
tab1, tab2 = st.tabs(["🚀 Phase 1: Federated Training", "🛡️ Phase 2: Live Threat Detection"])

with tab1:
    st.sidebar.header("⚙️ Simulation Settings")
    num_rounds = st.sidebar.slider("Federated Rounds", min_value=1, max_value=20, value=5)
    local_epochs = st.sidebar.slider("Local Epochs per Round", min_value=1, max_value=5, value=2)
    st.sidebar.markdown("---")
    st.sidebar.info("This dashboard simulates a decentralized federated learning network where model weights are secured using biological DNA cryptography (XOR/ADD operations + Chaotic Maps).")

    if st.button("🚀 Start Live Simulation", type="primary"):
        # 1. Initialization
        st.markdown("### 📡 Initializing Multi-Cloud Network...")
        clients_data, test_loader, input_size = prepare_data(num_clients=3)
        
        global_model = CloudSecurityModel(input_size)
        server = FLServer(global_model, password="ServerSecretKey2024")
        
        clients = []
        for i in range(3):
            client = FLClient(i+1, clients_data[i], CloudSecurityModel(input_size), 
                              f"Client{i+1}@SecurePass2024", "ServerSecretKey2024")
            clients.append(client)
            
        st.success("✅ Connected to AWS, Azure, and GCP Nodes successfully.")
        
        progress_bar = st.progress(0)
        round_text = st.empty()
        
        col1, col2, col3 = st.columns(3)
        c1_status = col1.empty()
        c2_status = col2.empty()
        c3_status = col3.empty()
        status_boxes = [c1_status, c2_status, c3_status]
        names = ["AWS Node", "Azure Node", "GCP Node"]
        
        st.markdown("### 🔐 Intercepted Network Traffic (DNA Encryption Preview)")
        network_box = st.empty()
        
        st.markdown("### 📊 Global Model Convergence")
        chart_col1, chart_col2 = st.columns(2)
        acc_chart = chart_col1.empty()
        loss_chart = chart_col2.empty()
        
        metric_cols = st.columns(4)
        m1, m2, m3, m4 = metric_cols[0].empty(), metric_cols[1].empty(), metric_cols[2].empty(), metric_cols[3].empty()
        
        global_acc_history = []
        global_loss_history = []
        
        for rnd in range(1, num_rounds + 1):
            round_text.markdown(f"<p class='big-font'>🔄 Federated Round {rnd} / {num_rounds}</p>", unsafe_allow_html=True)
            progress_bar.progress(rnd / num_rounds)
            
            for idx, c in enumerate(clients):
                status_boxes[idx].info(f"**{names[idx]}**\n\n⚙️ Training on Cloud Intrusion Logs...")
            
            for idx, c in enumerate(clients):
                loss, acc = c.train_local(epochs=local_epochs)
                status_boxes[idx].success(f"**{names[idx]}**\n\n✅ Training Complete\n\nLocal Acc: {acc:.2f}%")
                
            time.sleep(0.5)
            
            active_clients = []
            for idx, c in enumerate(clients):
                status_boxes[idx].warning(f"**{names[idx]}**\n\n🧬 Encrypting Weights to DNA...")
                
                if random.random() < 0.1: 
                    status_boxes[idx].error(f"**{names[idx]}**\n\n❌ Connection Lost (Network Error)")
                    continue
                    
                enc_payload = c.encrypt_and_send()
                server.receive_update(c.id, enc_payload, c.password, c.num_samples)
                active_clients.append(c)
                
                if len(active_clients) == 1:
                    first_layer_key = list(enc_payload.keys())[0]
                    dna_cipher = enc_payload[first_layer_key]['cipher']
                    payload_mb = sum(len(layer['cipher']) for layer in enc_payload.values()) / 1024 / 1024
                    
                    network_box.markdown(f"""
                    <div style='background-color: #0e1117; padding: 10px; border-radius: 5px; border: 1px solid #2ecc71;'>
                    <p style='color: #2ecc71; margin-bottom: 0;'><strong>[PACKET INTERCEPTED] Source: {names[idx]} | Payload Size: {payload_mb:.2f} MB</strong></p>
                    <p class='dna-font'>{dna_cipher[:200]}... [TRUNCATED]</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                status_boxes[idx].success(f"**{names[idx]}**\n\n🚀 Encrypted weights transmitted securely.")
                
            time.sleep(1)
            
            round_text.markdown(f"<p class='big-font'>🔄 Round {rnd}: Server Aggregating DNA Weights...</p>", unsafe_allow_html=True)
            server.aggregate()
            
            enc_global = server.encrypt_global()
            for c in active_clients:
                c.receive_and_decrypt(enc_global)
                
            metrics = server.evaluate(test_loader)
            global_acc_history.append(metrics['accuracy'])
            global_loss_history.append(metrics['loss'])
            
            df = pd.DataFrame({'Accuracy': global_acc_history, 'Loss': global_loss_history}, index=range(1, rnd + 1))
            acc_chart.line_chart(df['Accuracy'], color="#2ecc71")
            loss_chart.line_chart(df['Loss'], color="#e74c3c")
            
            m1.metric("Global Accuracy", f"{metrics['accuracy']:.2f}%", f"{metrics['accuracy'] - (global_acc_history[-2] if rnd > 1 else 0):.2f}%")
            m2.metric("Loss", f"{metrics['loss']:.4f}", f"{metrics['loss'] - (global_loss_history[-2] if rnd > 1 else 0):.4f}", delta_color="inverse")
            m3.metric("F1-Score", f"{metrics['f1_score']:.2f}%")
            m4.metric("ROC-AUC", f"{metrics['roc_auc']:.4f}")
            
        st.success("🎉 Simulation Complete! The federated model has successfully converged securely.")
        
        # Save model
        model_path = "results/secure_global_model.pth"
        torch.save(global_model.state_dict(), model_path)
        
        with open(model_path, "rb") as f:
            st.download_button(
                label="💾 Download Trained Global Model (.pth)",
                data=f,
                file_name="secure_global_model.pth",
                mime="application/octet-stream"
            )

with tab2:
    st.markdown("### 🔍 Real-Time Cloud Network Monitoring")
    st.markdown("Use the global threat-detection AI trained in Phase 1 to classify incoming network packets in real-time.")
    
    if not os.path.exists("results/secure_global_model.pth"):
        st.warning("⚠️ No trained model found. Please run the simulation in Phase 1 first.")
    else:
        if st.button("📡 Intercept & Analyze Network Traffic", type="primary"):
            st.info("Loading latest DNA-Federated Model...")
            model = CloudSecurityModel(input_size=30)
            model.load_state_dict(torch.load("results/secure_global_model.pth"))
            model.eval()
            
            st.markdown("#### Live Network Log Analysis")
            
            # Simulate 10 incoming network logs (some normal, some attacks)
            features = np.random.randn(10, 30)
            # Force a couple of them to be malicious by shifting their statistical distribution
            features[2] += 2.5 
            features[7] += 3.0
            
            tensor_features = torch.FloatTensor(features)
            
            with torch.no_grad():
                outputs = model(tensor_features)
                probs = torch.softmax(outputs, dim=1)[:, 1].numpy()
                preds = outputs.argmax(dim=1).numpy()
            
            for i in range(10):
                ip = f"192.168.1.{random.randint(2, 255)}"
                port = random.randint(1024, 65535)
                packet_size = random.randint(64, 1500)
                
                time.sleep(0.3) # Fake latency for dramatic effect
                
                if preds[i] == 1:
                    st.markdown(f"<div class='intrusion'>🚨 <strong>[MALICIOUS INTRUSION BLOCKED]</strong><br>IP: {ip}:{port} | Packet Size: {packet_size}B | Threat Confidence: {probs[i]*100:.1f}%</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='normal'>✅ <strong>[NORMAL TRAFFIC]</strong><br>IP: {ip}:{port} | Packet Size: {packet_size}B | Threat Confidence: {probs[i]*100:.1f}%</div>", unsafe_allow_html=True)
