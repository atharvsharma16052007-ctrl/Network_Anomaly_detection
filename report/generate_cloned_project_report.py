import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

base_dir = r"C:\Users\Atharv sharma\Desktop\coding\network-anomaly-detection"
doc_path_repo = os.path.join(base_dir, "report", "Netshield_Final_Project_Report.docx")
doc_path_report_docx = os.path.join(base_dir, "report", "Report.docx")
doc_path_desktop = r"C:\Users\Atharv sharma\Desktop\Netshield_Final_Project_Report.docx"
doc_path_synopsis = r"C:\Users\Atharv sharma\Desktop\Project_Synopsis.docx"
doc_path_attack = r"C:\Users\Atharv sharma\Desktop\AI_Based_Network_Attack_Forecasting.docx"
md_path = os.path.join(base_dir, "report", "Full_Academic_Project_Report.md")
cm_img = os.path.join(base_dir, "results", "confusion_matrix.png")
roc_img = os.path.join(base_dir, "results", "roc_curve.png")

doc = docx.Document()

# 1-inch margins
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

def set_para_font(p, font_name="Calibri", size_pt=11, color_rgb=(30, 41, 59), bold=False, italic=False, space_after=6, space_before=0, line_spacing=1.15):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    for run in p.runs:
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.font.color.rgb = RGBColor(*color_rgb)
        run.bold = bold
        run.italic = italic

def add_heading_num(doc, number_str, title_str):
    p = doc.add_paragraph()
    r1 = p.add_run(number_str + " ")
    r1.bold = True
    r2 = p.add_run(title_str)
    r2.bold = True
    set_para_font(p, font_name="Calibri", size_pt=15, color_rgb=(30, 58, 138), bold=True, space_before=16, space_after=6)
    return p

def add_subheading_num(doc, number_str, title_str):
    p = doc.add_paragraph()
    r1 = p.add_run(number_str + " ")
    r1.bold = True
    r2 = p.add_run(title_str)
    r2.bold = True
    set_para_font(p, font_name="Calibri", size_pt=12.5, color_rgb=(51, 65, 85), bold=True, space_before=10, space_after=4)
    return p

def add_body(doc, text):
    p = doc.add_paragraph()
    p.add_run(text)
    set_para_font(p, font_name="Calibri", size_pt=11, color_rgb=(30, 41, 59), bold=False, space_after=6)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p

def add_bullet(doc, title, text):
    p = doc.add_paragraph(style='List Bullet')
    r_bold = p.add_run(title + ": ")
    r_bold.bold = True
    p.add_run(text)
    set_para_font(p, font_name="Calibri", size_pt=11, color_rgb=(30, 41, 59), space_after=4)
    return p

def style_table(table, col_widths, headers, data):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        p = hdr_cells[i].paragraphs[0]
        if len(p.runs) > 0:
            p.runs[0].bold = True
            p.runs[0].font.name = "Calibri"
            p.runs[0].font.size = Pt(10)
            p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        shd = parse_xml(r'<w:shd {} w:fill="1E3A8A"/>'.format(nsdecls('w')))
        hdr_cells[i]._tc.get_or_add_tcPr().append(shd)
    
    for r_idx, row in enumerate(data):
        row_cells = table.add_row().cells
        fill_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            row_cells[c_idx].text = str(val)
            p = row_cells[c_idx].paragraphs[0]
            if len(p.runs) > 0:
                p.runs[0].font.name = "Calibri"
                p.runs[0].font.size = Pt(9.5)
                p.runs[0].font.color.rgb = RGBColor(30, 41, 59)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 or len(str(val)) > 30 else WD_ALIGN_PARAGRAPH.CENTER
            shd = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), fill_color))
            row_cells[c_idx]._tc.get_or_add_tcPr().append(shd)

    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = Inches(width)

# ==================== PAGE 1: COVER PAGE ====================
p1 = doc.add_paragraph()
p1.add_run("Lovely Professional University\nDepartment of Computer Science Engineering")
set_para_font(p1, font_name="Calibri", size_pt=15, color_rgb=(30, 58, 138), bold=True, space_before=24, space_after=18)
p1.alignment = WD_ALIGN_PARAGRAPH.CENTER

p2 = doc.add_paragraph()
p2.add_run("PROJECT SYNOPSIS")
set_para_font(p2, font_name="Calibri", size_pt=18, color_rgb=(100, 116, 139), bold=True, space_before=12, space_after=12)
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER

p3 = doc.add_paragraph()
p3.add_run("\"AI-Based Network Attack Forecasting from Network Traffic Data\"\n(Network Anomaly Detection & Netshield Console)")
set_para_font(p3, font_name="Calibri", size_pt=19, color_rgb=(30, 58, 138), bold=True, space_before=12, space_after=16)
p3.alignment = WD_ALIGN_PARAGRAPH.CENTER

p4 = doc.add_paragraph()
p4.add_run("Submitted in partial fulfillment of the requirements for the degree of\nB.Tech CSE - AI and ML")
set_para_font(p4, font_name="Calibri", size_pt=12, color_rgb=(71, 85, 105), italic=True, space_before=12, space_after=28)
p4.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Submitted By Table
t_sub = doc.add_table(rows=1, cols=2)
t_sub.alignment = WD_TABLE_ALIGNMENT.CENTER
t_sub.rows[0].cells[0].paragraphs[0].text = "Submitted By:"
t_sub.rows[0].cells[0].paragraphs[0].runs[0].bold = True
set_para_font(t_sub.rows[0].cells[0].paragraphs[0], font_name="Calibri", size_pt=11, color_rgb=(30, 58, 138), bold=True)
p_students = t_sub.rows[0].cells[1].paragraphs[0]
p_students.text = (
    "Atharv Sharma (Reg No: 12503900, Roll No: 61)\n"
    "Saiyam Passi (Reg No: 12528405, Roll No: 34)\n"
    "Tegbeer Singh (Reg No: 12517175, Roll No: 54)\n"
    "Sanskar Patwa (Reg No: 12520477, Roll No: 40)"
)
set_para_font(p_students, font_name="Calibri", size_pt=11, color_rgb=(30, 41, 59), line_spacing=1.2)
t_sub.rows[0].cells[0].width = Inches(2.2)
t_sub.rows[0].cells[1].width = Inches(4.3)

p5 = doc.add_paragraph()
p5.add_run("Under the Guidance of\nMr. Alan Alexander (AI Teacher)")
set_para_font(p5, font_name="Calibri", size_pt=12, color_rgb=(51, 65, 85), bold=True, space_before=28, space_after=12)
p5.alignment = WD_ALIGN_PARAGRAPH.CENTER

p6 = doc.add_paragraph()
p6.add_run("Academic Session: 2026–2027")
set_para_font(p6, font_name="Calibri", size_pt=11, color_rgb=(100, 116, 139), bold=True, space_before=6, space_after=24)
p6.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_page_break()

# ==================== 1. TITLE OF THE PROJECT ====================
add_heading_num(doc, "1.", "Title of the Project")
p_title = doc.add_paragraph()
p_title.add_run("AI-Based Network Attack Forecasting from Network Traffic Data\n").bold = True
set_para_font(p_title, font_name="Calibri", size_pt=12, color_rgb=(30, 58, 138), bold=True, space_after=4)

p_rat = doc.add_paragraph()
p_rat.add_run("Rationale: ").bold = True
p_rat.add_run(
    "This title reflects the core operation of the implemented cybersecurity project, which leverages an ensemble Random Forest "
    "machine learning classifier to autonomously analyze, predict, and classify malicious network connection telemetry in real-time."
)
set_para_font(p_rat, font_name="Calibri", size_pt=11, color_rgb=(30, 41, 59), space_after=12)

# ==================== 2. ABSTRACT ====================
add_heading_num(doc, "2.", "Abstract")
add_body(doc, 
    "The rapid growth of distributed cloud systems, modern enterprise networks, and connected digital infrastructures has created an urgent need for intelligent, automated cyber defense. Traditional signature-based Intrusion Detection Systems (IDS), such as legacy firewalls and rule-matching engines, are inherently reactive: they rely on predefined signatures of cataloged attacks and are fundamentally blind to zero-day vulnerabilities, polymorphic malware, and stealthy reconnaissance scans. Moreover, heuristic rule configurations frequently trigger overwhelming volumes of false positive alerts, leading to alert fatigue among Security Operations Center (SOC) personnel."
)
add_body(doc,
    "To overcome these operational vulnerabilities, this project implements a high-precision, AI-based Network Anomaly Detection System trained on the benchmark NSL-KDD dataset (125,974 network connection records across 41 granular features). The machine learning architecture utilizes an optimized Random Forest Classifier comprising 100 de-correlated decision trees with standardized feature scaling and categorical encoding. On an independent, unseen test partition of 25,195 network connection flows, the model achieves outstanding empirical performance: 99.90% classification accuracy, 99.96% precision, 99.83% recall, and an F1-score of 99.89%, with an Area Under the ROC Curve (AUC) of 1.0000. Crucially, the model generates only 4 false alarms out of 13,469 benign connections (an exceptionally low false positive rate of 0.029%), directly mitigating alert fatigue. Integrated within Netshield—a custom, responsive, light-mode defensive console—the system provides SOC analysts with zero mock data, persistent session audit logging, and exportable forensic CSV reports, delivering a robust, practical solution for modern enterprise cyber defense."
)

# ==================== 3. INTRODUCTION ====================
add_heading_num(doc, "3.", "Introduction")
add_body(doc, 
    "Network Intrusion Detection Systems (NIDS) serve as the frontline perimeter defense across contemporary cybersecurity architectures. Historically, enterprise network defense has relied almost exclusively on signature-matching engines (such as Snort or Suricata) that inspect incoming packet payloads against local databases of known threat signatures. While signature engines achieve near-zero false alarms on known threats, they are fundamentally incapable of recognizing novel zero-day attacks, encrypted malicious payloads, or mutated attack patterns."
)
add_body(doc, 
    "Machine Learning (ML) has emerged as an indispensable paradigm capable of transcending signature limitations. Rather than inspecting static byte sequences, machine learning models analyze multidimensional statistical telemetry from raw network flows—including connection duration, service protocol, flag status, source and destination byte counts, and host-level connection density. By learning the statistical boundaries of benign network traffic, an ensemble machine learning model can autonomously detect deviations that signify cyber attacks. In addition to core detection fidelity, modern security operations demand intuitive human-in-the-loop interfaces. This project develops an end-to-end detection pipeline coupled with Netshield, a production-grade operational console built for high-throughput SOC analysts."
)

# ==================== 4. PROBLEM STATEMENT ====================
add_heading_num(doc, "4.", "Problem Statement")
add_body(doc, "Conventional network intrusion detection architectures present several critical operational flaws:")
add_bullet(doc, "1. Inability to Detect Zero-Day & Novel Exploits", "Deterministic signature matchers cannot detect novel attack vectors before human security analysts manually inspect, reverse-engineer, and publish explicit signature rules.")
add_bullet(doc, "2. High False-Positive Rates & Operational Alert Fatigue", "Legacy heuristic detectors generate excessive false alarms on benign traffic variations, overwhelming SOC analysts and causing critical security breaches to be ignored.")
add_bullet(doc, "3. High Manual Maintenance Overhead", "Static rule libraries require continuous manual updating, patching, and tuning, creating high labor overhead and latency in threat neutralization.")
add_bullet(doc, "4. High-Dimensional Volume Scalability", "Modern multi-gigabit enterprise backbones generate millions of connection records daily. Rule-matching algorithms experience severe computational bottlenecks when scaling across high-dimensional feature spaces.")

# ==================== 5. AIM AND OBJECTIVES ====================
add_heading_num(doc, "5.", "Aim and Objectives")
add_subheading_num(doc, "5.1", "Aim")
add_body(doc, 
    "To design, train, evaluate, and deploy an autonomous, high-efficiency network anomaly detection and attack forecasting system utilizing an optimized Random Forest machine learning pipeline on benchmark network flow telemetry."
)

add_subheading_num(doc, "5.2", "Objectives")
add_bullet(doc, "Benchmark Dataset Ingestion & Analysis", "To acquire and explore the NSL-KDD benchmark dataset (125,974 records across 41 connection features) to evaluate feature distributions and traffic characteristics.")
add_bullet(doc, "Reproducible Preprocessing Pipeline", "To design and implement a non-leaking data preprocessing pipeline utilizing LabelEncoder for categorical variables (protocol_type, service, flag) and StandardScaler for numerical normalization.")
add_bullet(doc, "Ensemble Model Training & Tuning", "To train and optimize a Random Forest Classifier (100 estimators) to achieve high-throughput, sub-millisecond connection classification.")
add_bullet(doc, "Comprehensive Empirical Evaluation", "To validate the model across 25,195 unseen test samples utilizing Accuracy, Precision, Recall, F1-Score, Confusion Matrix, and ROC-AUC metrics.")
add_bullet(doc, "Pipeline Artifact Serialization", "To serialize the trained model, feature scalers, and label encoders into reusable Joblib binary artifacts for production serving.")
add_bullet(doc, "Netshield SOC Console Deployment", "To engineer and deploy an interactive, light-mode defensive console (Netshield) featuring zero mock data, dual-pipeline schema adaptability, session audit logging, and CSV export capabilities.")

# ==================== 6. LITERATURE REVIEW ====================
add_heading_num(doc, "6.", "Literature Review")
add_body(doc, 
    "A systematic review of existing cybersecurity literature highlights the evolutionary progression from rigid rule engines to ensemble machine learning in intrusion detection. Table 1 summarizes key research contributions, methodologies, and limitations."
)

# Table 1: Literature Review Table
t_lit = doc.add_table(rows=1, cols=4)
t_lit_headers = ["Author & Year", "Research Approach", "Key Findings", "Limitations"]
t_lit_data = [
    ["Tavallaee et al. (2009)", "Comprehensive analysis of KDD'99 and development of NSL-KDD.", "Eliminated 78% redundant records present in KDD Cup 1999, establishing an unbiased, balanced intrusion detection benchmark.", "Does not incorporate modern web protocols (HTTP/2, QUIC); remains an offline benchmark."],
    ["Sommer & Paxson (2010)", "Operational machine learning challenges in network intrusion detection.", "Identified the fundamental 'semantic gap' between ML anomaly scores and operational SOC requirements.", "Demonstrated that high false positive rates prevent automated intrusion blocking without human oversight."],
    ["Al Lail et al. (2023)", "Comparative study of ML algorithms for network intrusion detection.", "Demonstrated that ensemble tree models (Random Forest) outperform SVM, Naive Bayes, and single Decision Trees in accuracy and variance reduction.", "Evaluated models in isolated scripts without full-stack operational SOC deployment."],
    ["Sarhan et al. (2021)", "Feature engineering and NetFlow standardization for NIDS.", "Proved that statistical feature representation is often more critical than algorithm complexity.", "Deep learning models exhibited excessive inference latency compared to optimized tree ensembles."],
    ["Skopik et al. (2022)", "Behavior-based anomaly detection in telemetry logs.", "Validated that behavioral baselines can intercept unknown attack patterns without explicit signatures.", "Emphasized the challenge of concept drift and model maintenance in dynamic corporate networks."]
]
style_table(t_lit, [1.4, 1.8, 2.0, 1.8], t_lit_headers, t_lit_data)

add_body(doc, 
    "Research Gap: Existing intrusion detection research typically focuses exclusively on raw model metrics while neglecting real-world SOC usability. Most models exist as isolated scripts without interactive interfaces, persistence mechanisms, or multi-schema resilience. This project bridges this critical gap by delivering both an empirically verified Random Forest model (>99.9% accuracy) and a production-grade operational console (Netshield)."
)

# ==================== 7. EXISTING SYSTEM ====================
add_heading_num(doc, "7.", "Existing System")
add_bullet(doc, "Existing Techniques", "Industry standard Intrusion Detection Systems primarily employ signature pattern-matching engines (e.g., Snort, Suricata) and static firewall rules configured with predefined port and protocol filters.")
add_bullet(doc, "Advantages of Current Methods", "Signature engines achieve near-instant pattern matching with zero false alarms on previously cataloged legacy exploits.")
add_bullet(doc, "Limitations and Challenges", "Existing signature systems are completely blind to novel zero-day attacks, encrypted attack channels, and polymorphic malware. Furthermore, heuristic rule configurations cause severe alert fatigue among security analysts.")
add_bullet(doc, "Areas Needing Improvement", "There is an urgent requirement for intelligent behavioral anomaly tracking that can adapt to unknown traffic variations, minimize false positive alerts, and provide security teams with auditable forensic telemetry.")

# ==================== 8. PROPOSED SYSTEM ====================
add_heading_num(doc, "8.", "Proposed System")
add_body(doc, 
    "The proposed system, implemented directly within the project codebase, introduces an intelligent, end-to-end Machine Learning Network Anomaly Detection System paired with the Netshield operational console:"
)
add_bullet(doc, "Random Forest Machine Learning Engine", "An ensemble classifier of 100 de-correlated decision trees trained on 41 standardized network features to achieve sub-millisecond binary classification (Normal vs. Anomaly).")
add_bullet(doc, "Adaptive Dual-Pipeline Ingestion", "Netshield automatically detects the incoming dataset schema: 41-feature network flows are processed through the ML inference engine, while multi-column cybersecurity incident logs are routed to the threat telemetry analytics engine.")
add_bullet(doc, "Session Audit Ledger", "Every ingested file is assigned an immutable audit tracking code (e.g., ING-001, ING-002) recording sample sizes, anomaly rates, file names, and timestamps for regulatory compliance.")
add_bullet(doc, "Tailwind-Inspired Professional UI", "A clean, corporate light-mode dashboard designed with zero mock data, zero AI slop, and instant CSV forensic export.")

# ==================== 9. RESEARCH METHODOLOGY ====================
add_heading_num(doc, "9.", "Research Methodology")
add_body(doc, "The project implementation follows a structured seven-phase development workflow executed in Python:")
add_bullet(doc, "01_load_dataset.py", "Ingests the raw NSL-KDD benchmark CSV and inspects data types, record distributions, and column headers.")
add_bullet(doc, "02_explore_data.py", "Performs exploratory data analysis (EDA), generating feature histograms, null-value checks, and correlation matrices.")
add_bullet(doc, "03_preprocess.py", "Transforms categorical variables (protocol_type, service, flag) via LabelEncoder and scales 38 numeric attributes using StandardScaler.")
add_bullet(doc, "04_split_data.py", "Partitions the dataset into 100,779 training samples and 25,195 test samples using an 80/20 stratified split to preserve class balance.")
add_bullet(doc, "05_train_model.py", "Trains the RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1) across the training partition.")
add_bullet(doc, "06_evaluate_model.py", "Computes comprehensive evaluation metrics (Accuracy, Precision, Recall, F1) and generates high-resolution confusion matrix and ROC curve plots.")
add_bullet(doc, "07_save_model.py", "Persists model artifacts to models/random_forest_model.joblib for deployment within the Netshield dashboard.")

# ==================== 10. TOOLS AND TECHNOLOGIES REQUIRED ====================
add_heading_num(doc, "10.", "Tools and Technologies Required")
add_bullet(doc, "Programming Language", "Python 3.11 / Python 3.13")
add_bullet(doc, "Core ML & Data Libraries", "scikit-learn, pandas, numpy, joblib")
add_bullet(doc, "Visualization Libraries", "matplotlib, seaborn, plotly express, plotly.graph_objects")
add_bullet(doc, "Frontend Framework", "Streamlit with custom Tailwind CSS styling (#F8FAFC slate background, #FFFFFF cards, #1E3A8A headers)")
add_bullet(doc, "Benchmark Dataset", "NSL-KDD Benchmark Dataset (125,974 records across 41 granular connection features)")
add_bullet(doc, "Development Environment", "Visual Studio Code, Git / GitHub")
add_bullet(doc, "Hardware Specifications", "Minimum 8 GB RAM, Multi-core x86_64 CPU (AMD/Intel)")

# ==================== 11. SYSTEM ARCHITECTURE ====================
add_heading_num(doc, "11.", "System Architecture")

p_arch = doc.add_paragraph()
p_arch.add_run(
"""[Raw Network Traffic Data (CSV / Flow Telemetry)]
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
+-------------------------------------------------------+"""
)
set_para_font(p_arch, font_name="Courier New", size_pt=9.0, color_rgb=(30, 58, 138), space_before=6, space_after=10, line_spacing=1.05)

add_body(doc, 
    "Component Description: Incoming traffic passes through the automated schema detection module. When 41 connection features are detected, the payload is normalized via persisted scalers and evaluated by the Random Forest classifier. When high-level cybersecurity incident logs are provided, the system seamlessly redirects to the incident analytics pipeline. All actions are logged to the immutable session audit history."
)

# ==================== 12. EXPECTED OUTCOMES & EMPIRICAL METRICS ====================
add_heading_num(doc, "12.", "Expected Outcomes & Empirical Metrics")
add_bullet(doc, "Production ML Model", "A fully trained and optimized RandomForestClassifier serialized to models/random_forest_model.joblib.")
add_bullet(doc, "Quantitative ML Performance", "Evaluated on 25,195 unseen test samples, the system achieves 99.90% Accuracy, 99.96% Precision, 99.83% Recall, and an F1-Score of 99.89% with an AUC of 1.0000.")
add_bullet(doc, "Near-Zero False Positive Rate", "Out of 13,469 normal connections, only 4 were misclassified (0.029%), directly mitigating alert fatigue for SOC operators.")
add_bullet(doc, "Operational Console (Netshield)", "A functional, responsive web application (app.py) running locally on port 8501, featuring zero mock data, real-time filtering, and CSV export.")

# Table 2: Model Performance Table
t_eval = doc.add_table(rows=1, cols=5)
t_eval_headers = ["Traffic Class", "Precision", "Recall", "F1-Score", "Support (Sample Count)"]
t_eval_data = [
    ["Normal (Benign Traffic)", "0.9983 (99.83%)", "0.9997 (99.97%)", "0.9990 (99.90%)", "13,469"],
    ["Anomaly (Malicious Traffic)", "0.9996 (99.96%)", "0.9980 (99.80%)", "0.9989 (99.89%)", "11,726"],
    ["Macro Average", "0.9990 (99.90%)", "0.9990 (99.90%)", "0.9990 (99.90%)", "25,195"],
    ["Weighted Average", "0.9990 (99.90%)", "0.9990 (99.90%)", "0.9990 (99.90%)", "25,195"],
    ["Overall Model Accuracy", "-", "-", "0.9990 (99.90%)", "25,195"]
]
style_table(t_eval, [2.2, 1.1, 1.1, 1.1, 1.1], t_eval_headers, t_eval_data)

add_body(doc, 
    "Confusion Matrix Analysis: The empirical confusion matrix demonstrates almost perfect classification boundaries between benign network flows and cyber attacks across the 25,195 test records."
)

# Table 3: Confusion Matrix Table
t_cm = doc.add_table(rows=1, cols=3)
t_cm_headers = ["Actual Ground Truth", "Predicted Normal (Benign)", "Predicted Anomaly (Attack)"]
t_cm_data = [
    ["Actual Normal (13,469 samples)", "13,465 (True Negative - 99.97%)", "4 (False Positive - 0.03%)"],
    ["Actual Anomaly (11,726 samples)", "23 (False Negative - 0.20%)", "11,703 (True Positive - 99.80%)"]
]
style_table(t_cm, [2.5, 2.0, 2.0], t_cm_headers, t_cm_data)

# Embed images
if os.path.exists(cm_img):
    doc.add_paragraph()
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(cm_img, width=Inches(4.4))
    p_caption = doc.add_paragraph()
    p_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_caption.add_run("Figure 1: Confusion Matrix Heatmap for Random Forest Classifier (25,195 Test Records)")
    set_para_font(p_caption, font_name="Calibri", size_pt=9.5, color_rgb=(100, 116, 139), italic=True, space_after=12)

if os.path.exists(roc_img):
    doc.add_paragraph()
    p_img2 = doc.add_paragraph()
    p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img2.add_run().add_picture(roc_img, width=Inches(4.4))
    p_caption2 = doc.add_paragraph()
    p_caption2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_caption2.add_run("Figure 2: Receiver Operating Characteristic (ROC) Curve (AUC = 1.0000)")
    set_para_font(p_caption2, font_name="Calibri", size_pt=9.5, color_rgb=(100, 116, 139), italic=True, space_after=12)

# ==================== 13. APPLICATIONS AND SCOPE ====================
add_heading_num(doc, "13.", "Applications and Scope")
add_bullet(doc, "Real-world Applications", "")
p_app = doc.add_paragraph()
p_app.add_run(
    "• Security Operations Centers (SOC): Real-time triage of incoming network packet telemetry.\n"
    "• Cloud Infrastructure Defense: Anomaly detection within Virtual Private Cloud (VPC) flow logs.\n"
    "• Critical Infrastructure: Monitoring SCADA and industrial network communication for anomalous commands.\n"
    "• Academic & Research Labs: Providing an open benchmark testbed for evaluating intrusion detection models."
)
set_para_font(p_app, font_name="Calibri", size_pt=11, color_rgb=(30, 41, 59), line_spacing=1.2, space_after=6)

add_bullet(doc, "Scope Boundaries", "")
p_scope = doc.add_paragraph()
p_scope.add_run(
    "• In-Scope: Supervised classification of 41 flow features, dual-schema incident analytics, and local SOC visualization.\n"
    "• Out-of-Scope: Active deep-packet payload decryption (SSL/TLS inspection) and direct kernel-level packet dropping (firewall blocking)."
)
set_para_font(p_scope, font_name="Calibri", size_pt=11, color_rgb=(30, 41, 59), line_spacing=1.2, space_after=12)

# ==================== 14. PROJECT TIMELINE ====================
add_heading_num(doc, "14.", "Project Timeline")
t_time = doc.add_table(rows=1, cols=4)
t_time_headers = ["Phase", "Duration", "Key Activities / Milestones", "Deliverables"]
t_time_data = [
    ["Phase 1", "Weeks 1–2", "Problem formulation, threat landscape review, environment setup", "Architecture specification, git repository"],
    ["Phase 2", "Weeks 3–4", "Dataset ingestion (NSL-KDD), exploratory data analysis (EDA)", "Cleaned data summary, feature correlation graphs"],
    ["Phase 3", "Weeks 5–6", "Data preprocessing, LabelEncoder, StandardScaler scaling", "Preprocessed feature matrices, train/test split"],
    ["Phase 4", "Weeks 7–10", "Random Forest model training, hyperparameter optimization", "Trained model artifact (network_anomaly_model.pkl)"],
    ["Phase 5", "Weeks 11–12", "Model evaluation, confusion matrix & ROC curve generation", "Evaluation reports, metrics validation"],
    ["Phase 6", "Weeks 13–14", "Netshield dashboard development, dual-schema support, final testing", "Production Netshield application (app.py), Final Report"]
]
style_table(t_time, [1.0, 1.2, 2.5, 2.3], t_time_headers, t_time_data)

# ==================== 15. CONCLUSION ====================
add_heading_num(doc, "15.", "Conclusion")
add_body(doc, 
    "This project successfully designs, implements, and critically evaluates an intelligent Network Anomaly Detection System and defensive telemetry dashboard (Netshield). Utilizing an optimized Random Forest classifier trained on 125,974 NSL-KDD benchmark records, the model achieved 99.90% classification accuracy, 99.96% precision, and an AUC of 1.0000 on 25,195 unseen test connections. Furthermore, the development of Netshield demonstrates how machine learning algorithms can be embedded within an enterprise-ready SOC interface featuring zero mock data, dual-pipeline schema adaptability, and persistent session audit logging. The project conclusively validates the viability of machine learning in modern cyber defense while establishing clear pathways for real-time live streaming integration."
)

# ==================== 16. REFERENCES ====================
add_heading_num(doc, "16.", "References")

references = [
    ("[1]", "M. Tavallaee, E. Bagheri, W. Lu, and A. A. Ghorbani", "2009", "A detailed analysis of the KDD CUP 99 data set", "2009 IEEE Symposium on Computational Intelligence for Security and Defense Applications, pp. 53-58"),
    ("[2]", "R. Sommer and V. Paxson", "2010", "Outside the Closed World: On Using Machine Learning for Network Intrusion Detection", "2010 IEEE Symposium on Security and Privacy, Oakland, CA, USA, pp. 305-316"),
    ("[3]", "M. Al Lail, A. Garcia, and S. Olivo", "2023", "Machine Learning for Network Intrusion Detection—A Comparative Study", "Future Internet, vol. 15, no. 7, p. 243"),
    ("[4]", "Ö. Aslan, S. S. Aktuğ, M. O. Okay, A. A. Yilmaz, and E. Akin", "2023", "A Comprehensive Review of Cyber Security Vulnerabilities, Threats, Attacks, and Solutions", "Electronics, vol. 12, no. 6, pp. 1-42"),
    ("[5]", "M. Sarhan, S. Layeghy, N. Moustafa, and M. Portmann", "2021", "NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems", "IEEE Transactions on Network and Service Management, vol. 18, no. 1, pp. 117-135"),
    ("[6]", "Y. Kumar and V. Kumar", "2023", "A Systematic Review on Intrusion Detection System in Wireless Networks: Variants, Attacks, and Applications", "Wireless Personal Communications, vol. 133, no. 1, pp. 395-452"),
    ("[7]", "F. Skopik, M. Wurzenberger, G. Höld, M. Landauer, and W. Kuhn", "2022", "Behavior-Based Anomaly Detection in Log Data of Physical Access Control Systems", "IEEE Transactions on Dependable and Secure Computing, vol. 19, no. 5, pp. 3197-3212"),
    ("[8]", "E. Shamsinejad, T. Banirostam, M. M. Pedram, and A. M. Rahmani", "2024", "A Review of Anonymization Algorithms and Methods in Big Data", "Annals of Data Science, pp. 1-28")
]

for ref_id, authors, year, title, source in references:
    p_ref = doc.add_paragraph()
    p_ref.add_run(f"{ref_id} ").bold = True
    p_ref.add_run(f"{authors}, ")
    p_ref.add_run(f"\"{title},\" ").italic = True
    p_ref.add_run(f"{source}, {year}.")
    set_para_font(p_ref, font_name="Calibri", size_pt=10, color_rgb=(51, 65, 85), space_after=4)

# Save to all target paths
doc.save(doc_path_repo)
doc.save(doc_path_report_docx)
doc.save(doc_path_desktop)
doc.save(doc_path_synopsis)
doc.save(doc_path_attack)

print("Saved DOCX successfully to all target locations:")
print(" -", doc_path_synopsis)
print(" -", doc_path_desktop)
print(" -", doc_path_report_docx)
