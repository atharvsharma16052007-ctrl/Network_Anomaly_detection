# Netshield: AI-Driven Network Traffic Anomaly & Threat Detection System

[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg)](https://python.org)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.0+-F7931E.svg)](https://scikit-learn.org)
[![Tailwind CSS](https://img.shields.io/badge/UI-Tailwind%20CSS%20Light-06B6D4.svg)](https://tailwindcss.com)

**Netshield** is an enterprise-grade cyber telemetry inspection platform and network intrusion detection engine. Built for real-world Security Operations Centers (SOC) and Smart India Hackathon (SIH) demonstrations, Netshield provides multi-schema telemetry ingestion, deep packet inspection, volumetric flow analytics, and a **Two-Stage Threat Profiling Engine** that translates low-level anomalies into plain-English attack types, severity ratings, detection triggers, and mitigation playbooks.

---

## 📌 Key Capabilities

- **Zero-Preloaded Traffic Policy**: Operates in a clean state upon launch. Users dynamically ingest CSV captures via drag-and-drop or file selection.
- **Two-Stage Threat Profiler**:
  - **Stage 1 (Anomaly Detection)**: High-speed Random Forest and decision boundary models detect binary deviation from normal operational baselines.
  - **Stage 2 (Threat Classification & Playbook)**: Evaluates TCP/IP flags, error rate signatures, volumetric packet metrics, and service targets to categorize threats into plain-English classifications (SYN Flood, Port Sweep, Slowloris, Host Compromise, Brute Force, etc.) with explicit severity ratings (`CRITICAL`, `HIGH`, `MEDIUM`, `NORMAL`).
- **Interactive SOC Dashboards**:
  - Donut distribution of threat severity ratings.
  - Frequency distribution of identified attack vectors.
  - Full tabular audit trail with search, sort, and CSV export.
  - Session ingestion history tracking each analyzed dataset.
  - Built-in Attack Types Reference Manual.
- **Dual Deployment Architecture**:
  - **Local Python/Streamlit Engine**: Runs natively on `http://localhost:8501`.
  - **Client-Side Mirror Engine**: Standalone `index.html` + `app.js` configured for static zero-server hosting (e.g., Vercel).

---

## 🚀 Quick Start: Running on Localhost:8501

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/atharvsharma16052007-ctrl/Network_Anomaly_detection.git
cd Network_Anomaly_detection
```

### 2️⃣ Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Launch the Netshield Console on Port 8501
```bash
streamlit run app.py --server.port 8501
```
Open your browser and navigate to:
👉 **[http://localhost:8501](http://localhost:8501)**

---

## 🌐 Alternative: Running the Static Web Mirror

For client-side zero-python environments or Vercel deployments:
1. Open `index.html` directly in any web browser, or serve it with any static HTTP server:
   ```bash
   npx serve .
   ```
2. The web frontend identically mirrors the `localhost:8501` Python application using pure browser-based parsing and Plotly.js charts.

---

## 📂 Project Architecture

```
network-anomaly-detection/
├── app.py                         # Main Streamlit SOC Application (runs at localhost:8501)
├── app.js                         # Web telemetry logic (mirrors app.py for browser execution)
├── index.html                     # Standalone HTML5 dashboard
├── style.css                      # Tailwind-styled clean light corporate theme
├── vercel.json                    # Vercel deployment configuration
├── requirements.txt               # Complete Python runtime dependencies
├── NETSHIELD_Presentation.pptx    # Official 10-slide SIH project presentation deck
├── SPEAKER_PREPARATION_GUIDE.md   # Comprehensive speaker prep & viva defense guide
├── frontend/                      # Standalone web mirror bundle
│   ├── index.html
│   ├── app.js
│   └── style.css
├── models/                        # Serialized ML models & preprocessors
│   ├── network_anomaly_model.pkl  # Trained Random Forest classifier
│   ├── encoders.pkl               # Protocol & service categorical encoders
│   └── scaler.pkl                 # Robust feature standard scaler
├── dataset/                       # Sample telemetry CSVs for live demonstration
│   ├── sample_traffic.csv         # Standard test packet telemetry
│   ├── user_test_input.csv        # Custom test input file
│   └── Global_Cybersecurity_Threats_2015-2024.csv
└── results/                       # Model evaluation benchmarks & confusion matrix
```

---

## 🧠 Two-Stage Threat Profiling Specification

When an anomaly is flagged by the machine learning model, Netshield initiates secondary heuristic rule mapping:

| Attack Vector | Heuristic Profile Triggers | Threat Severity | Immediate Mitigation Action |
| :--- | :--- | :--- | :--- |
| **SYN Flood (DoS)** | Flag `S0` + `serror_rate > 0.5` + High connection count | 🔴 **CRITICAL** | Rate-limit SYN packets; enable TCP SYN cookies; drop attacking IP at edge firewall. |
| **Port Sweep / Recon** | `dst_host_diff_srv_rate > 0.5` + Multi-port probing | 🟠 **HIGH** | Temporarily block source IP; enforce stealth port filtering; alert SOC analysts. |
| **Slowloris Connection Starvation** | Session duration > 100s + `dst_bytes < 50` | 🟠 **HIGH** | Enforce aggressive HTTP keep-alive timeouts; limit connections per client IP. |
| **Privilege Escalation (U2R)** | `root_shell > 0` or `su_attempted > 0` or compromised count | 🔴 **CRITICAL** | Immediately quarantine host; terminate unauthorized shells; rotate root credentials. |
| **Brute Force Infiltration** | `num_failed_logins >= 2` or guest login anomaly | 🟡 **MEDIUM** | Trigger exponential authentication backoff; enforce MFA; isolate target daemon. |

---

## 🎤 Presentation & Speaker Resources

- **Presentation Deck**: Download the 10-slide 16:9 widescreen presentation deck: [`NETSHIELD_Presentation.pptx`](./NETSHIELD_Presentation.pptx)
- **Speaker Preparation & Q&A Defense Guide**: Detailed slide-by-slide speaker scripts, technical deep dives, and answers to expected evaluator questions: [`SPEAKER_PREPARATION_GUIDE.md`](./SPEAKER_PREPARATION_GUIDE.md)

---

## 📄 License
This project is open-source under the MIT License for educational and Smart India Hackathon (SIH) research purposes.
