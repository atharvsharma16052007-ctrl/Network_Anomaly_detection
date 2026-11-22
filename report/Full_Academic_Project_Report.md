# Lovely Professional University
### Department of Computer Science Engineering

## PROJECT SYNOPSIS
### "AI-Based Network Attack Forecasting from Network Traffic Data"
*(Network Anomaly Detection & Netshield Console)*

**Submitted in partial fulfillment of the requirements for the degree of**  
**B.Tech CSE - AI and ML**

**Submitted By:**  
- **Atharv Sharma** (Reg No: 12503900, Roll No: 61)  
- **Saiyam Passi** (Reg No: 12528405, Roll No: 34)  
- **Tegbeer Singh** (Reg No: 12517175, Roll No: 54)  
- **Sanskar Patwa** (Reg No: 12520477, Roll No: 40)  

**Under the Guidance of:**  
**Mr. Alan Alexander (AI Teacher)**  

**Academic Session:** 2026–2027  

---

## 1. Title of the Project
**AI-Based Network Attack Forecasting from Network Traffic Data**  
*Rationale:* This title reflects the core operation of the implemented cybersecurity project, which leverages an ensemble Random Forest machine learning classifier to autonomously analyze, predict, and classify malicious network connection telemetry in real-time.

---

## 2. Abstract
The rapid growth of distributed cloud systems, modern enterprise networks, and connected digital infrastructures has created an urgent need for intelligent, automated cyber defense. Traditional signature-based Intrusion Detection Systems (IDS), such as legacy firewalls and rule-matching engines, are inherently reactive: they rely on predefined signatures of cataloged attacks and are fundamentally blind to zero-day vulnerabilities, polymorphic malware, and stealthy reconnaissance scans. Moreover, heuristic rule configurations frequently trigger overwhelming volumes of false positive alerts, leading to alert fatigue among Security Operations Center (SOC) personnel.

To overcome these operational vulnerabilities, this project implements a high-precision, AI-based Network Anomaly Detection System trained on the benchmark NSL-KDD dataset (125,974 network connection records across 41 granular features). The machine learning architecture utilizes an optimized Random Forest Classifier comprising 100 de-correlated decision trees with standardized feature scaling and categorical encoding. On an independent, unseen test partition of 25,195 network connection flows, the model achieves outstanding empirical performance: **99.90% classification accuracy, 99.96% precision, 99.83% recall, and an F1-score of 99.89%**, with an Area Under the ROC Curve (AUC) of **1.0000**. Crucially, the model generates only 4 false alarms out of 13,469 benign connections (an exceptionally low false positive rate of 0.029%), directly mitigating alert fatigue. Integrated within Netshield—a custom, responsive, light-mode defensive console—the system provides SOC analysts with zero mock data, persistent session audit logging, and exportable forensic CSV reports, delivering a robust, practical solution for modern enterprise cyber defense.

---

## 3. Introduction
Network Intrusion Detection Systems (NIDS) serve as the frontline perimeter defense across contemporary cybersecurity architectures. Historically, enterprise network defense has relied almost exclusively on signature-matching engines (such as Snort or Suricata) that inspect incoming packet payloads against local databases of known threat signatures. While signature engines achieve near-zero false alarms on known threats, they are fundamentally incapable of recognizing novel zero-day attacks, encrypted malicious payloads, or mutated attack patterns.

Machine Learning (ML) has emerged as an indispensable paradigm capable of transcending signature limitations. Rather than inspecting static byte sequences, machine learning models analyze multidimensional statistical telemetry from raw network flows—including connection duration, service protocol, flag status, source and destination byte counts, and host-level connection density. By learning the statistical boundaries of benign network traffic, an ensemble machine learning model can autonomously detect deviations that signify cyber attacks. In addition to core detection fidelity, modern security operations demand intuitive human-in-the-loop interfaces. This project develops an end-to-end detection pipeline coupled with Netshield, a production-grade operational console built for high-throughput SOC analysts.

---

## 4. Problem Statement
Conventional network intrusion detection architectures present several critical operational flaws:
1. **Inability to Detect Zero-Day & Novel Exploits:** Deterministic signature matchers cannot detect novel attack vectors before human security analysts manually inspect, reverse-engineer, and publish explicit signature rules.
2. **High False-Positive Rates & Operational Alert Fatigue:** Legacy heuristic detectors generate excessive false alarms on benign traffic variations, overwhelming SOC analysts and causing critical security breaches to be ignored.
3. **High Manual Maintenance Overhead:** Static rule libraries require continuous manual updating, patching, and tuning, creating high labor overhead and latency in threat neutralization.
4. **High-Dimensional Volume Scalability:** Modern multi-gigabit enterprise backbones generate millions of connection records daily. Rule-matching algorithms experience severe computational bottlenecks when scaling across high-dimensional feature spaces.

---

## 5. Aim and Objectives

### 5.1 Aim
To design, train, evaluate, and deploy an autonomous, high-efficiency network anomaly detection and attack forecasting system utilizing an optimized Random Forest machine learning pipeline on benchmark network flow telemetry.

### 5.2 Objectives
- **Benchmark Dataset Ingestion & Analysis:** To acquire and explore the NSL-KDD benchmark dataset (125,974 records across 41 connection features) to evaluate feature distributions and traffic characteristics.
- **Reproducible Preprocessing Pipeline:** To design and implement a non-leaking data preprocessing pipeline utilizing `LabelEncoder` for categorical variables (`protocol_type`, `service`, `flag`) and `StandardScaler` for numerical normalization.
- **Ensemble Model Training & Tuning:** To train and optimize a Random Forest Classifier (100 estimators) to achieve high-throughput, sub-millisecond connection classification.
- **Comprehensive Empirical Evaluation:** To validate the model across 25,195 unseen test samples utilizing Accuracy, Precision, Recall, F1-Score, Confusion Matrix, and ROC-AUC metrics.
- **Pipeline Artifact Serialization:** To serialize the trained model, feature scalers, and label encoders into reusable Joblib binary artifacts (`network_anomaly_model.pkl`) for production serving.
- **Netshield SOC Console Deployment:** To engineer and deploy an interactive, light-mode defensive console (Netshield) featuring zero mock data, dual-pipeline schema adaptability, session audit logging, and CSV export capabilities.

---

## 6. Literature Review
A systematic review of existing cybersecurity literature highlights the evolutionary progression from rigid rule engines to ensemble machine learning in intrusion detection.

| Author & Year | Research Approach | Key Findings | Limitations |
| :--- | :--- | :--- | :--- |
| **Tavallaee et al. (2009)** | Comprehensive analysis of KDD'99 and development of NSL-KDD. | Eliminated 78% redundant records present in KDD Cup 1999, establishing an unbiased, balanced intrusion detection benchmark. | Does not incorporate modern web protocols (HTTP/2, QUIC); remains an offline benchmark. |
| **Sommer & Paxson (2010)** | Operational machine learning challenges in network intrusion detection. | Identified the fundamental 'semantic gap' between ML anomaly scores and operational SOC requirements. | Demonstrated that high false positive rates prevent automated intrusion blocking without human oversight. |
| **Al Lail et al. (2023)** | Comparative study of ML algorithms for network intrusion detection. | Demonstrated that ensemble tree models (Random Forest) outperform SVM, Naive Bayes, and single Decision Trees in accuracy and variance reduction. | Evaluated models in isolated scripts without full-stack operational SOC deployment. |
| **Sarhan et al. (2021)** | Feature engineering and NetFlow standardization for NIDS. | Proved that statistical feature representation is often more critical than algorithm complexity. | Deep learning models exhibited excessive inference latency compared to optimized tree ensembles. |
| **Skopik et al. (2022)** | Behavior-based anomaly detection in telemetry logs. | Validated that behavioral baselines can intercept unknown attack patterns without explicit signatures. | Emphasized the challenge of concept drift and model maintenance in dynamic corporate networks. |

**Research Gap:** Existing intrusion detection research typically focuses exclusively on raw model metrics while neglecting real-world SOC usability. Most models exist as isolated scripts without interactive interfaces, persistence mechanisms, or multi-schema resilience. This project bridges this critical gap by delivering both an empirically verified Random Forest model (>99.9% accuracy) and a production-grade operational console (Netshield).

---

## 7. Existing System
- **Existing Techniques:** Industry standard Intrusion Detection Systems primarily employ signature pattern-matching engines (e.g., Snort, Suricata) and static firewall rules configured with predefined port and protocol filters.
- **Advantages of Current Methods:** Signature engines achieve near-instant pattern matching with zero false alarms on previously cataloged legacy exploits.
- **Limitations and Challenges:** Existing signature systems are completely blind to novel zero-day attacks, encrypted attack channels, and polymorphic malware. Furthermore, heuristic rule configurations cause severe alert fatigue among security analysts.
- **Areas Needing Improvement:** There is an urgent requirement for intelligent behavioral anomaly tracking that can adapt to unknown traffic variations, minimize false positive alerts, and provide security teams with auditable forensic telemetry.

---

## 8. Proposed System
The proposed system, implemented directly within the project codebase, introduces an intelligent, end-to-end Machine Learning Network Anomaly Detection System paired with the Netshield operational console:
- **Random Forest Machine Learning Engine:** An ensemble classifier of 100 de-correlated decision trees trained on 41 standardized network features to achieve sub-millisecond binary classification (Normal vs. Anomaly).
- **Adaptive Dual-Pipeline Ingestion:** Netshield automatically detects the incoming dataset schema: 41-feature network flows are processed through the ML inference engine, while multi-column cybersecurity incident logs are routed to the threat telemetry analytics engine.
- **Session Audit Ledger:** Every ingested file is assigned an immutable audit tracking code (e.g., `ING-001`, `ING-002`) recording sample sizes, anomaly rates, file names, and timestamps for regulatory compliance.
- **Tailwind-Inspired Professional UI:** A clean, corporate light-mode dashboard designed with zero mock data, zero AI slop, and instant CSV forensic export.

---

## 9. Research Methodology
The project implementation follows a structured seven-phase development workflow executed in Python:
- **01_load_dataset.py:** Ingests the raw NSL-KDD benchmark CSV and inspects data types, record distributions, and column headers.
- **02_explore_data.py:** Performs exploratory data analysis (EDA), generating feature histograms, null-value checks, and correlation matrices.
- **03_preprocess.py:** Transforms categorical variables (`protocol_type`, `service`, `flag`) via `LabelEncoder` and scales 38 numeric attributes using `StandardScaler`.
- **04_split_data.py:** Partitions the dataset into 100,779 training samples and 25,195 test samples using an 80/20 stratified split to preserve class balance.
- **05_train_model.py:** Trains the `RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)` across the training partition.
- **06_evaluate_model.py:** Computes comprehensive evaluation metrics (Accuracy, Precision, Recall, F1) and generates high-resolution confusion matrix and ROC curve plots.
- **07_save_model.py:** Persists model artifacts to `models/random_forest_model.joblib` / `network_anomaly_model.pkl` for deployment within the Netshield dashboard.

---

## 10. Tools and Technologies Required
- **Programming Language:** Python 3.11 / Python 3.13
- **Core ML & Data Libraries:** `scikit-learn`, `pandas`, `numpy`, `joblib`
- **Visualization Libraries:** `matplotlib`, `seaborn`, `plotly express`, `plotly.graph_objects`
- **Frontend Framework:** Streamlit with custom Tailwind CSS styling (`#F8FAFC` slate background, `#FFFFFF` cards, `#1E3A8A` headers)
- **Benchmark Dataset:** NSL-KDD Benchmark Dataset (125,974 records across 41 granular connection features)
- **Development Environment:** Visual Studio Code, Git / GitHub
- **Hardware Specifications:** Minimum 8 GB RAM, Multi-core x86_64 CPU (AMD/Intel)

---

## 11. System Architecture
```
[Raw Network Traffic Data (CSV / Flow Telemetry)]
                    |
                    v
+-------------------------------------------------------+
| Ingestion & Schema Detection Engine (Netshield UI)    |
| - Inspects column headers (41 features vs Incidents)  |
+-------------------------------------------------------+
        |                                       |
  [41 Features]                        [Incident Data]
        v                                       v
+------------------------------+     +-------------------------------+
| Feature Transformation       |     | Telemetry Analytics Engine    |
| - LabelEncoder (protocol)    |     | - Threat Type Distribution    |
| - StandardScaler (38 floats) |     | - Industry Financial Loss     |
+------------------------------+     +-------------------------------+
        |                                       |
        v                                       |
+------------------------------+                |
| Random Forest Inference      |                |
| - 100 Decision Tree Ensemble |                |
| - Predicts: Normal / Anomaly |                |
+------------------------------+                |
        |                                       |
        +-------------------+-------------------+
                            |
                            v
+-------------------------------------------------------+
| Netshield Defensive Console & Audit Trail             |
| - Real-Time Anomaly KPIs (Total, Normal, Attack, Rate)|
| - Session Audit History Ledger (ING-001, ING-002)     |
| - Filterable Forensic Table & CSV Export              |
+-------------------------------------------------------+
```
*Component Description:* Incoming traffic passes through the automated schema detection module. When 41 connection features are detected, the payload is normalized via persisted scalers and evaluated by the Random Forest classifier. When high-level cybersecurity incident logs are provided, the system seamlessly redirects to the incident analytics pipeline. All actions are logged to the immutable session audit history.

---

## 12. Expected Outcomes & Empirical Metrics
- **Production ML Model:** A fully trained and optimized `RandomForestClassifier` serialized to `models/network_anomaly_model.pkl`.
- **Quantitative ML Performance:** Evaluated on 25,195 unseen test samples, the system achieves **99.90% Accuracy, 99.96% Precision, 99.83% Recall, and an F1-Score of 99.89% with an AUC of 1.0000**.
- **Near-Zero False Positive Rate:** Out of 13,469 normal connections, only 4 were misclassified (0.029%), directly mitigating alert fatigue for SOC operators.
- **Operational Console (Netshield):** A functional, responsive web application (`app.py`) running locally on port 8501, featuring zero mock data, real-time filtering, and CSV export.

### Detailed Model Classification Performance Table
| Traffic Class | Precision | Recall | F1-Score | Support (Sample Count) |
| :--- | :--- | :--- | :--- | :--- |
| **Normal (Benign Traffic)** | 0.9983 (99.83%) | 0.9997 (99.97%) | 0.9990 (99.90%) | 13,469 |
| **Anomaly (Malicious Traffic)** | 0.9996 (99.96%) | 0.9980 (99.80%) | 0.9989 (99.89%) | 11,726 |
| **Macro Average** | 0.9990 (99.90%) | 0.9990 (99.90%) | 0.9990 (99.90%) | 25,195 |
| **Weighted Average** | 0.9990 (99.90%) | 0.9990 (99.90%) | 0.9990 (99.90%) | 25,195 |
| **Overall Model Accuracy** | - | - | **0.9990 (99.90%)** | **25,195** |

### Confusion Matrix Breakdown
| Actual Ground Truth | Predicted Normal (Benign) | Predicted Anomaly (Attack) |
| :--- | :--- | :--- |
| **Actual Normal (13,469 samples)** | **13,465** (True Negative - 99.97%) | **4** (False Positive - 0.03%) |
| **Actual Anomaly (11,726 samples)** | **23** (False Negative - 0.20%) | **11,703** (True Positive - 99.80%) |

![Confusion Matrix](file:///C:/Users/Atharv%20sharma/Desktop/coding/network-anomaly-detection/results/confusion_matrix.png)
*Figure 1: Confusion Matrix Heatmap for Random Forest Classifier (25,195 Test Records)*

![ROC Curve](file:///C:/Users/Atharv%20sharma/Desktop/coding/network-anomaly-detection/results/roc_curve.png)
*Figure 2: Receiver Operating Characteristic (ROC) Curve (AUC = 1.0000)*

---

## 13. Applications and Scope
**Real-world Applications:**
- **Security Operations Centers (SOC):** Real-time triage of incoming network packet telemetry.
- **Cloud Infrastructure Defense:** Anomaly detection within Virtual Private Cloud (VPC) flow logs.
- **Critical Infrastructure:** Monitoring SCADA and industrial network communication for anomalous commands.
- **Academic & Research Labs:** Providing an open benchmark testbed for evaluating intrusion detection models.

**Scope Boundaries:**
- *In-Scope:* Supervised classification of 41 flow features, dual-schema incident analytics, and local SOC visualization.
- *Out-of-Scope:* Active deep-packet payload decryption (SSL/TLS inspection) and direct kernel-level packet dropping (firewall blocking).

---

## 14. Project Timeline
| Phase | Duration | Key Activities / Milestones | Deliverables |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Weeks 1–2 | Problem formulation, threat landscape review, environment setup | Architecture specification, git repository |
| **Phase 2** | Weeks 3–4 | Dataset ingestion (NSL-KDD), exploratory data analysis (EDA) | Cleaned data summary, feature correlation graphs |
| **Phase 3** | Weeks 5–6 | Data preprocessing, LabelEncoder, StandardScaler scaling | Preprocessed feature matrices, train/test split |
| **Phase 4** | Weeks 7–10 | Random Forest model training, hyperparameter optimization | Trained model artifact (`network_anomaly_model.pkl`) |
| **Phase 5** | Weeks 11–12 | Model evaluation, confusion matrix & ROC curve generation | Evaluation reports, metrics validation |
| **Phase 6** | Weeks 13–14 | Netshield dashboard development, dual-schema support, final testing | Production Netshield application (`app.py`), Final Report |

---

## 15. Conclusion
This project successfully designs, implements, and critically evaluates an intelligent Network Anomaly Detection System and defensive telemetry dashboard (Netshield). Utilizing an optimized Random Forest classifier trained on 125,974 NSL-KDD benchmark records, the model achieved **99.90% classification accuracy, 99.96% precision, and an AUC of 1.0000** on 25,195 unseen test connections. Furthermore, the development of Netshield demonstrates how machine learning algorithms can be embedded within an enterprise-ready SOC interface featuring zero mock data, dual-pipeline schema adaptability, and persistent session audit logging. The project conclusively validates the viability of machine learning in modern cyber defense while establishing clear pathways for real-time live streaming integration.

---

## 16. References
1. **M. Tavallaee, E. Bagheri, W. Lu, and A. A. Ghorbani**, *"A detailed analysis of the KDD CUP 99 data set,"* 2009 IEEE Symposium on Computational Intelligence for Security and Defense Applications, pp. 53-58, 2009.
2. **R. Sommer and V. Paxson**, *"Outside the Closed World: On Using Machine Learning for Network Intrusion Detection,"* 2010 IEEE Symposium on Security and Privacy, Oakland, CA, USA, pp. 305-316, 2010.
3. **M. Al Lail, A. Garcia, and S. Olivo**, *"Machine Learning for Network Intrusion Detection—A Comparative Study,"* Future Internet, vol. 15, no. 7, p. 243, 2023.
4. **Ö. Aslan, S. S. Aktuğ, M. O. Okay, A. A. Yilmaz, and E. Akin**, *"A Comprehensive Review of Cyber Security Vulnerabilities, Threats, Attacks, and Solutions,"* Electronics, vol. 12, no. 6, pp. 1-42, 2023.
5. **M. Sarhan, S. Layeghy, N. Moustafa, and M. Portmann**, *"NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems,"* IEEE Transactions on Network and Service Management, vol. 18, no. 1, pp. 117-135, 2021.
6. **Y. Kumar and V. Kumar**, *"A Systematic Review on Intrusion Detection System in Wireless Networks: Variants, Attacks, and Applications,"* Wireless Personal Communications, vol. 133, no. 1, pp. 395-452, 2023.
7. **F. Skopik, M. Wurzenberger, G. Höld, M. Landauer, and W. Kuhn**, *"Behavior-Based Anomaly Detection in Log Data of Physical Access Control Systems,"* IEEE Transactions on Dependable and Secure Computing, vol. 19, no. 5, pp. 3197-3212, 2022.
8. **E. Shamsinejad, T. Banirostam, M. M. Pedram, and A. M. Rahmani**, *"A Review of Anonymization Algorithms and Methods in Big Data,"* Annals of Data Science, pp. 1-28, 2024.
