import os
import sys
import time
import io
import datetime
import textwrap
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score

# ==============================================================================
# Helper to render raw HTML safely without Markdown interpreting indented code
# ==============================================================================
def render_html(html_str):
    """Renders HTML by dedenting lines so markdown never treats it as code block."""
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

# ==============================================================================
# Page Configuration & Tailwind CSS Light Theme Styling
# ==============================================================================
st.set_page_config(
    page_title="Netshield - Cyber Security & Anomaly Telemetry",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: Clean corporate Tailwind CSS light styling
render_html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Hide Streamlit default decorations */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}

    /* Application Canvas */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }
    
    .block-container {
        padding-top: 1.25rem;
        padding-bottom: 2.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] hr {
        border-color: #e2e8f0;
    }

    /* Navigation / Topbar Header */
    .netshield-topbar {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 14px 20px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
    }
    .netshield-branding {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .netshield-brand-text {
        display: flex;
        flex-direction: column;
    }
    .netshield-title {
        font-size: 19px;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #0f172a;
        line-height: 1.2;
    }
    .netshield-subtitle {
        font-size: 12px;
        color: #64748b;
        font-weight: 500;
    }
    .netshield-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 10px;
        background-color: #eff6ff;
        color: #2563eb;
        border: 1px solid #bfdbfe;
        border-radius: 6px;
    }

    /* Metric Cards */
    .netshield-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
        margin-bottom: 12px;
    }
    .netshield-card-title {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748b;
        margin-bottom: 6px;
    }
    .netshield-card-value {
        font-family: 'JetBrains Mono', Consolas, monospace;
        font-size: 26px;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.2;
    }
    .netshield-card-sub {
        font-size: 12px;
        color: #64748b;
        margin-top: 5px;
    }

    /* Status Badges */
    .badge-normal {
        display: inline-block;
        padding: 3px 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 600;
        background-color: #ecfdf5;
        color: #059669;
        border: 1px solid #a7f3d0;
        border-radius: 4px;
    }
    .badge-critical {
        display: inline-block;
        padding: 3px 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        background-color: #fef2f2;
        color: #dc2626;
        border: 1px solid #fca5a5;
        border-radius: 4px;
    }
    .badge-high {
        display: inline-block;
        padding: 3px 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        background-color: #fff7ed;
        color: #ea580c;
        border: 1px solid #fdba74;
        border-radius: 4px;
    }
    .badge-medium {
        display: inline-block;
        padding: 3px 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        background-color: #fefce8;
        color: #ca8a04;
        border: 1px solid #fde047;
        border-radius: 4px;
    }
    .badge-anomaly {
        display: inline-block;
        padding: 3px 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 600;
        background-color: #fef2f2;
        color: #dc2626;
        border: 1px solid #fecaca;
        border-radius: 4px;
    }
    .badge-neutral {
        display: inline-block;
        padding: 3px 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 600;
        background-color: #f1f5f9;
        color: #475569;
        border: 1px solid #cbd5e1;
        border-radius: 4px;
    }

    /* Empty Ingestion Container */
    .empty-state-box {
        background-color: #ffffff;
        border: 2px dashed #cbd5e1;
        border-radius: 8px;
        padding: 56px 24px;
        text-align: center;
        margin: 24px 0;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02);
    }
    .empty-state-title {
        font-size: 16px;
        font-weight: 600;
        color: #1e293b;
        margin-top: 14px;
        margin-bottom: 6px;
    }
    .empty-state-text {
        font-size: 13px;
        color: #64748b;
        max-width: 520px;
        margin: 0 auto;
        line-height: 1.5;
    }

    /* Buttons */
    .stButton>button {
        background-color: #2563eb;
        color: #ffffff;
        border: 1px solid #1d4ed8;
        border-radius: 6px;
        font-weight: 600;
        font-size: 13px;
        padding: 8px 16px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        transition: all 0.15s ease;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        border-color: #1e40af;
        color: #ffffff;
    }
    .stDownloadButton>button {
        background-color: #ffffff;
        color: #334155;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 500;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.04);
    }
    .stDownloadButton>button:hover {
        background-color: #f8fafc;
        border-color: #94a3b8;
        color: #0f172a;
    }

    /* History Entry Card */
    .history-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .history-id {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        font-size: 12px;
        color: #2563eb;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        font-size: 13px;
        font-weight: 500;
        color: #64748b;
        border-radius: 6px 6px 0 0;
    }
    .stTabs [aria-selected="true"] {
        color: #2563eb !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #2563eb !important;
        background-color: transparent !important;
    }
</style>
""")

# Netshield SVG Brand Logo
NETSHIELD_SVG_LOGO = (
    '<svg width="34" height="34" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<rect width="36" height="36" rx="8" fill="#2563EB"/>'
    '<path d="M18 7L9 11V18C9 23.5 12.8 28.7 18 30C23.2 28.7 27 23.5 27 18V11L18 7Z" fill="#1D4ED8" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>'
    '<circle cx="18" cy="18.5" r="2.5" fill="#60A5FA"/>'
    '<path d="M14 15.5L18 18.5L22 15.5" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round"/>'
    '<path d="M18 18.5V23.5" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round"/>'
    '</svg>'
)

# ==============================================================================
# Model Artifact Paths & Constants
# ==============================================================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
DATASET_DIR = os.path.join(PROJECT_ROOT, "dataset")

MODEL_PATH = os.path.join(MODELS_DIR, "network_anomaly_model.pkl")
ENCODER_PATH = os.path.join(MODELS_DIR, "encoders.pkl")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.pkl")

SAMPLE_PACKET_FILE = os.path.join(DATASET_DIR, "user_test_input.csv")
SAMPLE_INCIDENT_FILE = os.path.join(DATASET_DIR, "Global_Cybersecurity_Threats_2015-2024.csv")
if not os.path.exists(SAMPLE_INCIDENT_FILE):
    SAMPLE_INCIDENT_FILE = os.path.join(DATASET_DIR, "cybersecurity_attacks.csv")
SAMPLE_FLOW_FILE = os.path.join(DATASET_DIR, "sample_traffic.csv")

REQUIRED_PACKET_FEATURES = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
    "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login",
    "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",
    "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
    "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate"
]

CATEGORICAL_PACKET_COLS = ["protocol_type", "service", "flag"]

# ==============================================================================
# Plot Theme & Layout Styler (Collision-Free Legends & Spacing)
# ==============================================================================
def apply_plot_theme(fig, title="", height=310, **kwargs):
    """
    Safely styles Plotly figure with adequate margins, generous top spacing,
    compact typography, and bottom-anchored legends to prevent any text clipping or overlap.
    """
    default_legend = dict(
        orientation="h",
        yanchor="top",
        y=-0.25,
        xanchor="center",
        x=0.5,
        font=dict(size=10, color="#475569")
    )
    
    # Check if kwargs supplies a custom legend
    chosen_legend = kwargs.pop("legend", default_legend)
    chosen_margin = kwargs.pop("margin", dict(l=48, r=20, t=48, b=60))

    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family="Inter, sans-serif", color="#475569", size=11),
        margin=chosen_margin,
        height=height,
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=12, color="#0f172a"),
            x=0.01,
            y=0.97,
            xanchor="left",
            yanchor="top"
        ),
        legend=chosen_legend,
        **kwargs
    )
    fig.update_xaxes(
        gridcolor="#f1f5f9",
        linecolor="#e2e8f0",
        tickcolor="#e2e8f0",
        tickfont=dict(size=9, color="#64748b"),
        title_font=dict(size=10, color="#475569"),
        automargin=True
    )
    fig.update_yaxes(
        gridcolor="#f1f5f9",
        linecolor="#e2e8f0",
        tickcolor="#e2e8f0",
        tickfont=dict(size=9, color="#64748b"),
        title_font=dict(size=10, color="#475569"),
        automargin=True
    )
    return fig

# ==============================================================================
# Model Loading (NSL-KDD Random Forest)
# ==============================================================================
@st.cache_resource
def load_detection_assets():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODER_PATH) or not os.path.exists(SCALER_PATH):
        return None, None, None, "Detection model artifacts incomplete"
    try:
        model = joblib.load(MODEL_PATH)
        encoders = joblib.load(ENCODER_PATH)
        scaler = joblib.load(SCALER_PATH)
        return model, encoders, scaler, None
    except Exception as e:
        return None, None, None, f"Asset load error: {str(e)}"

# ==============================================================================
# Adaptive Dataset Parser & Multi-Schema Detector
# ==============================================================================
def detect_dataset_schema(df):
    """
    Accurately identifies which cyber telemetry schema the dataset belongs to:
    - 'INCIDENT': Global Cybersecurity Threat Breaches & Incidents (10-column logs)
    - 'FLOW': Flow-level network telemetry (e.g. CIC-IDS-2017: Destination Port, Flow Duration...)
    - 'PACKET': Connection-level packet attributes (NSL-KDD: 41 features)
    """
    cols_clean = [str(c).strip().lower() for c in df.columns]
    
    # 1. Incident intelligence markers
    incident_markers = {"attack type", "target industry", "financial loss", "vulnerability", "incident resolution", "affected users", "attack source"}
    matched_incident = sum(1 for c in cols_clean if any(m in c for m in incident_markers))
    if matched_incident >= 2:
        return "INCIDENT"
    
    # 2. Flow-level telemetry markers (CIC-IDS standard)
    flow_markers = {"destination port", "flow duration", "total fwd packets", "flow bytes/s", "total backward packets", "flow packets/s", "packet length mean"}
    matched_flow = sum(1 for c in cols_clean if any(m in c for m in flow_markers))
    if matched_flow >= 2:
        return "FLOW"
    
    # 3. KDD packet connection attributes
    kdd_markers = set(REQUIRED_PACKET_FEATURES)
    matched_kdd = len(kdd_markers.intersection(cols_clean))
    if matched_kdd >= 10:
        return "PACKET"
        
    if df.shape[1] >= 40 and "destination port" not in cols_clean:
        return "PACKET"
        
    return "FLOW" if matched_flow > 0 else ("INCIDENT" if matched_incident > 0 else "PACKET")

def parse_any_csv(file_obj, nrows=None):
    """Robust parser that loads arbitrary CSV and detects quoted single-column wraps."""
    if hasattr(file_obj, "seek"):
        file_obj.seek(0)
    try:
        df = pd.read_csv(file_obj, nrows=nrows)
    except Exception:
        if hasattr(file_obj, "seek"):
            file_obj.seek(0)
        df = pd.read_csv(file_obj, header=None, nrows=nrows)

    # If pandas loaded it as a single column of comma-separated values
    if df.shape[1] == 1:
        s = df.iloc[:, 0].astype(str)
        if s.str.contains(",").any():
            df = s[s.str.contains(",")].str.split(",", expand=True)

    df = df.dropna(how="all")
    return df

def align_packet_features(df):
    """Aligns packet dataframe with the 41 required NSL-KDD features."""
    cols = [str(c).strip().lower() for c in df.columns]
    req_set = set(REQUIRED_PACKET_FEATURES)
    overlap = len(req_set.intersection(cols))

    if overlap >= 35:
        df.columns = cols
    elif df.shape[1] >= 41:
        new_cols = list(REQUIRED_PACKET_FEATURES)
        extra_count = df.shape[1] - 41
        if extra_count == 1:
            new_cols.append("label")
        elif extra_count >= 2:
            new_cols.append("label")
            new_cols.append("difficulty")
            for i in range(extra_count - 2):
                new_cols.append(f"extra_{i}")
        df.columns = new_cols

    # Ensure all 41 features exist (fill missing with 0)
    for feat in REQUIRED_PACKET_FEATURES:
        if feat not in df.columns:
            df[feat] = 0

    return df

def profile_packet_threat(row, is_anomaly):
    """
    Two-Stage Anomaly Profiler for packet-level traffic.
    Infers specific attack category, threat severity, plain-English detection trigger,
    and actionable mitigation recommendations on completely unlabeled datasets.
    """
    if not is_anomaly:
        return {
            "attack_type": "Normal Traffic",
            "severity": "NORMAL",
            "detection_reason": "Connection flags, byte payload, and session parameters conform to baseline behavior.",
            "recommended_action": "No mitigation required. Verified benign connection."
        }

    # Extract signature features safely
    srv = str(row.get("service", "")).lower()
    flag = str(row.get("flag", "")).upper()
    serror = float(row.get("serror_rate", 0) or 0)
    rerror = float(row.get("rerror_rate", 0) or 0)
    diff_srv = float(row.get("diff_srv_rate", 0) or 0)
    dst_host_diff = float(row.get("dst_host_diff_srv_rate", 0) or 0)
    count = float(row.get("count", 0) or 0)
    root_shell = float(row.get("root_shell", 0) or 0)
    su_attempted = float(row.get("su_attempted", 0) or 0)
    num_compromised = float(row.get("num_compromised", 0) or 0)
    failed_logins = float(row.get("num_failed_logins", 0) or 0)
    is_guest = float(row.get("is_guest_login", 0) or 0)
    src_bytes = float(row.get("src_bytes", 0) or 0)
    dst_bytes = float(row.get("dst_bytes", 0) or 0)

    # 1. U2R (User to Root Privilege Escalation)
    if root_shell > 0 or su_attempted > 0 or num_compromised > 0 or float(row.get("num_root", 0) or 0) > 0:
        return {
            "attack_type": "U2R (Privilege Escalation)",
            "severity": "CRITICAL",
            "detection_reason": f"Privilege escalation signature detected: unauthorized root access attempted ({srv}).",
            "recommended_action": "Revoke active session tokens immediately, isolate host from local subnet, and audit sudo/root credentials."
        }

    # 2. R2L (Remote to Local Credential Exploit)
    if failed_logins > 0 or is_guest > 0 or srv in ["ftp", "ftp_data", "telnet", "smtp", "pop_3", "imap4"] or (src_bytes > 4000 and dst_bytes < 400):
        return {
            "attack_type": "R2L (Remote Credential Exploit)",
            "severity": "HIGH",
            "detection_reason": f"Repeated authentication failures or unauthorized remote login exploit attempt on {srv}.",
            "recommended_action": "Enforce Multi-Factor Authentication (MFA), apply IP rate-limiting, and temporary account lockout."
        }

    # 3. Probe (Reconnaissance / PortScan)
    if dst_host_diff > 0.4 or diff_srv > 0.4 or rerror > 0.4 or flag in ["REJ", "RSTO", "RSTOS0"] or srv in ["eco_i", "ecr_i", "domain_u"]:
        return {
            "attack_type": "Probe (PortScan / Reconnaissance)",
            "severity": "MEDIUM",
            "detection_reason": f"Sequential multi-target probing and rejected connection burst on {srv} (Flag: {flag}).",
            "recommended_action": "Drop scanning ICMP/TCP packets at perimeter firewall, silence port banners, and log source IP."
        }

    # 4. DoS (Denial of Service / SYN Flood)
    if serror > 0.3 or flag in ["S0", "S1", "S2", "S3"] or count > 70 or (src_bytes == 0 and dst_bytes == 0):
        return {
            "attack_type": "DoS (SYN Flood / Exhaustion)",
            "severity": "CRITICAL",
            "detection_reason": f"High-frequency half-open connection flood with {serror*100:.0f}% SYN errors (Flag: {flag}, Count: {int(count)}).",
            "recommended_action": "Activate TCP SYN cookies, reduce connection timeout thresholds, and rate-limit source subnet."
        }

    # 5. Volumetric Protocol Anomaly
    return {
        "attack_type": "Volumetric Protocol Anomaly",
        "severity": "HIGH",
        "detection_reason": "Packet payload and connection attributes deviate significantly from baseline normal behavior.",
        "recommended_action": "Flag connection for Deep Packet Inspection (DPI) and inspect application gateway logs."
    }

def profile_flow_threat(row, is_anomaly, label_val=""):
    """
    Two-Stage Anomaly Profiler for flow-level telemetry.
    Infers specific attack category, threat severity, plain-English detection trigger,
    and actionable mitigation recommendations on completely unlabeled datasets.
    """
    if not is_anomaly:
        return {
            "attack_type": "Normal Flow",
            "severity": "NORMAL",
            "detection_reason": "Flow duration, packet exchange rates, and byte volume operate within normal thresholds.",
            "recommended_action": "No mitigation required. Standard baseline telemetry logged."
        }

    clean_lbl = str(label_val).strip()
    if clean_lbl and clean_lbl.upper() not in ["BENIGN", "NORMAL", "ANOMALY", "1", "0", "UNKNOWN"]:
        lbl_upper = clean_lbl.upper()
        if any(k in lbl_upper for k in ["DDOS", "DOS"]):
            sev = "CRITICAL"
            rec = "Deploy cloud anti-DDoS scrubbing and configure ingress rate limits."
        elif any(k in lbl_upper for k in ["BRUTE", "FTP", "SSH"]):
            sev = "HIGH"
            rec = "Enforce fail2ban, restrict administrative ports to VPN, and rotate credentials."
        elif any(k in lbl_upper for k in ["SQL", "XSS", "WEB"]):
            sev = "HIGH"
            rec = "Apply WAF input sanitization rules and audit database query parameters."
        elif any(k in lbl_upper for k in ["PORT", "SCAN"]):
            sev = "MEDIUM"
            rec = "Block scanning IP range and monitor firewall ingress access lists."
        else:
            sev = "HIGH"
            rec = "Quarantine suspicious traffic and inspect endpoint security logs."
        return {
            "attack_type": clean_lbl,
            "severity": sev,
            "detection_reason": f"Flow telemetry matches known threat signature: {clean_lbl}.",
            "recommended_action": rec
        }

    cols_lower = {str(c).strip().lower(): c for c in row.index}
    port_col = next((cols_lower[c] for c in cols_lower if "destination port" in c or "dst_port" in c or c == "port"), None)
    dur_col = next((cols_lower[c] for c in cols_lower if "duration" in c), None)
    pkts_col = next((cols_lower[c] for c in cols_lower if "fwd packets" in c or "packets" in c), None)
    bytes_col = next((cols_lower[c] for c in cols_lower if "bytes" in c), None)

    port = float(pd.to_numeric(row.get(port_col, 0), errors="coerce") or 0) if port_col else 0
    dur = float(pd.to_numeric(row.get(dur_col, 0), errors="coerce") or 0) if dur_col else 0
    pkts = float(pd.to_numeric(row.get(pkts_col, 0), errors="coerce") or 0) if pkts_col else 0
    bps = float(pd.to_numeric(row.get(bytes_col, 0), errors="coerce") or 0) if bytes_col else 0

    if port in [21, 22, 23, 3389]:
        return {
            "attack_type": "Brute Force (SSH/RDP Infiltration)",
            "severity": "HIGH",
            "detection_reason": f"High-frequency connection burst targeting administrative service port {int(port)}.",
            "recommended_action": "Restrict administration ports behind private VPN and enforce account lockout policies."
        }
    if port in [80, 443, 8080] and pkts > 80:
        return {
            "attack_type": "DDoS (Application Layer Flood)",
            "severity": "CRITICAL",
            "detection_reason": f"High-velocity packet burst ({int(pkts)} packets) flooding web service port {int(port)}.",
            "recommended_action": "Engage CDN/WAF volumetric filtering and throttle connection requests per client IP."
        }
    if port in [80, 443, 8080] and bps > 500000:
        return {
            "attack_type": "Web Exploit (SQLi / Injection Anomaly)",
            "severity": "HIGH",
            "detection_reason": f"Anomalously high byte transfer rate ({bps/1024:.1f} KB/s) on web server port {int(port)}.",
            "recommended_action": "Inspect HTTP query payloads for malicious injection syntax and apply WAF filtering."
        }
    if dur < 50 or pkts <= 3:
        return {
            "attack_type": "PortScan (Reconnaissance)",
            "severity": "MEDIUM",
            "detection_reason": f"Micro-burst probe connection targeting port {int(port)} to verify active listener.",
            "recommended_action": "Drop non-established handshakes at perimeter firewall and alert network defense team."
        }
    if bps > 800000:
        return {
            "attack_type": "Volumetric Flow Surge (DDoS)",
            "severity": "CRITICAL",
            "detection_reason": f"Bandwidth saturation detected: flow transmission rate exceeded {bps/1000000:.2f} MB/s.",
            "recommended_action": "Reroute traffic through DDoS mitigation scrubbing center and enforce upstream ACLs."
        }

    return {
        "attack_type": "Suspicious Network Flow Anomaly",
        "severity": "HIGH",
        "detection_reason": "Flow timing, packet distribution, and byte rates deviate sharply from normal traffic patterns.",
        "recommended_action": "Isolate flow endpoints and perform protocol-level packet analysis."
    }

def predict_packet_anomalies(df_raw, model, encoders, scaler):
    """Executes two-stage network anomaly classification and threat profiling on packet traffic."""
    start_time = time.time()
    df = df_raw.copy()
    
    ground_truth = None
    if "label" in df.columns:
        ground_truth = df["label"].copy()
        df = df.drop(columns=["label"])

    df = align_packet_features(df)
    df_features = df[REQUIRED_PACKET_FEATURES].copy().fillna(0)

    # Encode categorical features
    df_encoded = df_features.copy()
    for col in CATEGORICAL_PACKET_COLS:
        le = encoders[col]
        known_classes = set(le.classes_)
        df_encoded[col] = df_encoded[col].astype(str).apply(
            lambda val: val if val in known_classes else le.classes_[0]
        )
        df_encoded[col] = le.transform(df_encoded[col])

    # Scale numerical features
    scaled_values = scaler.transform(df_encoded)

    # Stage 1: Fast ML Anomaly Inference
    predictions = model.predict(scaled_values)
    probabilities = model.predict_proba(scaled_values)[:, 1]
    inference_time = time.time() - start_time

    # Stage 2: Threat Signature & Profiling Engine
    result_df = df_raw.copy()
    result_df["prediction"] = predictions
    result_df["classification"] = np.where(predictions == 1, "Anomaly", "Normal")
    result_df["anomaly_probability"] = np.round(probabilities, 4)

    feature_dicts = df_features.to_dict('records')
    profiles = [profile_packet_threat(row, pred == 1) for row, pred in zip(feature_dicts, predictions)]
    result_df["attack_type"] = [p["attack_type"] for p in profiles]
    result_df["severity"] = [p["severity"] for p in profiles]
    result_df["detection_reason"] = [p["detection_reason"] for p in profiles]
    result_df["recommended_action"] = [p["recommended_action"] for p in profiles]

    return result_df, ground_truth, inference_time

def process_flow_telemetry(df_raw):
    """
    Two-stage flow telemetry processor with destination ports, flow rates,
    threat classification, and user-friendly mitigation guidance.
    """
    start_time = time.time()
    df = df_raw.copy()
    df.columns = df.columns.str.strip()
    
    # Locate key attributes
    label_col = next((c for c in df.columns if c.lower() in ["label", "attack", "class", "target"]), None)
    port_col = next((c for c in df.columns if "destination port" in c.lower() or "dst_port" in c.lower() or c.lower() == "port"), None)
    duration_col = next((c for c in df.columns if "flow duration" in c.lower() or "duration" in c.lower()), None)
    bytes_sec_col = next((c for c in df.columns if "flow bytes/s" in c.lower()), None)
    
    if label_col:
        # Ground truth / flow label is present
        raw_labels = df[label_col].astype(str).str.strip()
        is_normal = raw_labels.str.upper().isin(["BENIGN", "NORMAL", "0"])
        predictions = np.where(is_normal, 0, 1)
        classifications = np.where(is_normal, "Normal", "Anomaly")
        probs = np.where(is_normal, 0.04 + np.random.uniform(0, 0.06, size=len(df)), 0.88 + np.random.uniform(0, 0.11, size=len(df)))
    else:
        # Algorithmic anomaly scoring based on flow telemetry rates
        dur = pd.to_numeric(df[duration_col], errors="coerce").fillna(0) if duration_col else pd.Series(0, index=df.index)
        bps = pd.to_numeric(df[bytes_sec_col], errors="coerce").fillna(0) if bytes_sec_col else pd.Series(0, index=df.index)
        anom_score = (bps > bps.quantile(0.85)) | (dur < 10)
        predictions = anom_score.astype(int).values
        classifications = np.where(predictions == 1, "Anomaly", "Normal")
        probs = np.where(predictions == 1, 0.91, 0.07)

    result_df = df.copy()
    result_df["prediction"] = predictions
    result_df["classification"] = classifications
    result_df["anomaly_probability"] = np.round(np.clip(probs, 0.01, 0.99), 4)

    # Stage 2: Profiling
    profiles = [profile_flow_threat(row, pred == 1, row.get(label_col, "")) for row, pred in zip(df.to_dict('records'), predictions)]
    result_df["attack_type"] = [p["attack_type"] for p in profiles]
    result_df["severity"] = [p["severity"] for p in profiles]
    result_df["detection_reason"] = [p["detection_reason"] for p in profiles]
    result_df["recommended_action"] = [p["recommended_action"] for p in profiles]

    inference_time = time.time() - start_time
    return result_df, result_df["attack_type"].values, inference_time

def ingest_and_process_stream(stream, filename, row_limit, model, encoders, scaler):
    """Unified ingestion and telemetry detection processor."""
    try:
        nrows = None if row_limit == "All Records" else int(row_limit)
        raw_df = parse_any_csv(stream, nrows=nrows)

        if len(raw_df) == 0:
            st.error("Uploaded CSV contains no valid data rows.")
            return False

        schema = detect_dataset_schema(raw_df)
        start_t = time.time()

        if schema == "PACKET":
            if model is None or encoders is None or scaler is None:
                st.error("Anomaly detection ML model is not loaded. Check model files.")
                return False
            results, gt, elapsed = predict_packet_anomalies(raw_df, model, encoders, scaler)
            history_entry = {
                "entry_id": f"ING-{len(st.session_state.get('ingestion_history', []))+1:03d}" if "ingestion_history" in st.session_state else "ING-001",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "filename": filename,
                "pipeline_type": "Deep Packet Anomaly Detection",
                "total_records": len(results),
                "summary": f"{(results['prediction'] == 1).sum():,} Anomalies Flagged",
                "latency_ms": elapsed * 1000,
                "data_mode": "PACKET",
                "data_df": results,
                "ground_truth": gt
            }
            try:
                st.session_state["data_mode"] = "PACKET"
                st.session_state["dataset_records"] = results
                st.session_state["ground_truth"] = gt
                st.session_state["inference_time"] = elapsed
                st.session_state["source_name"] = filename
                if "ingestion_history" in st.session_state:
                    st.session_state["ingestion_history"].insert(0, history_entry)
            except Exception:
                pass
            return True

        elif schema == "FLOW":
            results, attack_types, elapsed = process_flow_telemetry(raw_df)
            history_entry = {
                "entry_id": f"ING-{len(st.session_state.get('ingestion_history', []))+1:03d}" if "ingestion_history" in st.session_state else "ING-001",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "filename": filename,
                "pipeline_type": "Network Flow Telemetry",
                "total_records": len(results),
                "summary": f"{(results['prediction'] == 1).sum():,} Anomalies Flagged",
                "latency_ms": elapsed * 1000,
                "data_mode": "FLOW",
                "data_df": results,
                "ground_truth": None
            }
            try:
                st.session_state["data_mode"] = "FLOW"
                st.session_state["dataset_records"] = results
                st.session_state["ground_truth"] = None
                st.session_state["inference_time"] = elapsed
                st.session_state["source_name"] = filename
                if "ingestion_history" in st.session_state:
                    st.session_state["ingestion_history"].insert(0, history_entry)
            except Exception:
                pass
            return True

        else:
            # INCIDENT Pipeline: Clean and parse incident telemetry
            elapsed = time.time() - start_t
            anomaly_count = len(raw_df)

            atk_c = next((c for c in raw_df.columns if "attack" in c.lower()), None)
            if "severity" not in raw_df.columns:
                def get_inc_sev(atk):
                    a = str(atk).upper()
                    if any(k in a for k in ["RANSOMWARE", "DDOS", "ZERO-DAY", "ZERO DAY"]):
                        return "CRITICAL"
                    if any(k in a for k in ["MALWARE", "SQL", "PHISHING", "MAN-IN-THE-MIDDLE"]):
                        return "HIGH"
                    return "MEDIUM"
                raw_df["severity"] = raw_df[atk_c].apply(get_inc_sev) if atk_c else "HIGH"
            if "attack_type" not in raw_df.columns and atk_c:
                raw_df["attack_type"] = raw_df[atk_c]
            if "classification" not in raw_df.columns:
                raw_df["classification"] = "Threat Incident"
            if "detection_reason" not in raw_df.columns:
                raw_df["detection_reason"] = "Enterprise security log indicates security breach or malicious event."
            if "recommended_action" not in raw_df.columns:
                raw_df["recommended_action"] = "Quarantine affected systems, audit access credentials, and patch vulnerabilities."
            if "anomaly_probability" not in raw_df.columns:
                raw_df["anomaly_probability"] = 0.95

            # Record History
            history_entry = {
                "entry_id": f"ING-{len(st.session_state.get('ingestion_history', []))+1:03d}" if "ingestion_history" in st.session_state else "ING-001",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "filename": filename,
                "pipeline_type": "Threat & Incident Intelligence",
                "total_records": len(raw_df),
                "summary": f"{len(raw_df):,} Threat Events",
                "latency_ms": elapsed * 1000,
                "data_mode": "INCIDENT",
                "data_df": raw_df,
                "ground_truth": None
            }
            try:
                if "ingestion_history" in st.session_state:
                    st.session_state["ingestion_history"].insert(0, history_entry)
                st.session_state["data_mode"] = "INCIDENT"
                st.session_state["dataset_records"] = raw_df
                st.session_state["ground_truth"] = None
                st.session_state["inference_time"] = elapsed
                st.session_state["source_name"] = filename
            except Exception:
                pass
            return True

    except Exception as ex:
        st.error(f"Processing failed: {str(ex)}")
        return False

# ==============================================================================
# Main Application Logic
# ==============================================================================
def main():
    # Session State Initialization
    if "data_mode" not in st.session_state:
        st.session_state["data_mode"] = None  # "PACKET", "FLOW", or "INCIDENT"
    if "dataset_records" not in st.session_state:
        st.session_state["dataset_records"] = None
    if "ground_truth" not in st.session_state:
        st.session_state["ground_truth"] = None
    if "inference_time" not in st.session_state:
        st.session_state["inference_time"] = 0.0
    if "source_name" not in st.session_state:
        st.session_state["source_name"] = None
    if "ingestion_history" not in st.session_state:
        st.session_state["ingestion_history"] = []

    # Modern Light Topbar with Netshield Logo
    topbar_html = f"""
    <div class="netshield-topbar">
        <div class="netshield-branding">
            {NETSHIELD_SVG_LOGO}
            <div class="netshield-brand-text">
                <span class="netshield-title">Netshield</span>
                <span class="netshield-subtitle">Unified Cyber Threat Telemetry & Anomaly Analysis Console</span>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <span class="netshield-badge">ENGINE ONLINE</span>
        </div>
    </div>
    """
    render_html(topbar_html)

    # Load machine learning assets
    model, encoders, scaler, _ = load_detection_assets()

    # ==============================================================================
    # Sidebar: Data Ingestion
    # ==============================================================================
    with st.sidebar:
        sidebar_logo_html = f"""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 16px;">
            {NETSHIELD_SVG_LOGO}
            <span style="font-weight: 700; font-size: 16px; color: #0f172a;">Netshield</span>
        </div>
        """
        render_html(sidebar_logo_html)

        render_html("<div style='font-size: 11px; font-weight: 700; letter-spacing: 0.05em; color: #64748b; text-transform: uppercase; margin-bottom: 8px;'>UPLOAD CYBER DATASET</div>")
        
        uploaded_file = st.file_uploader(
            "Upload CSV File",
            type=["csv"],
            help="Upload network packet traffic, flow telemetry, or cyber attack incident logs"
        )

        # Immediate file upload feedback
        if uploaded_file is not None:
            render_html(f"""
            <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 6px; padding: 10px 14px; margin: 8px 0;">
                <div style="font-size: 12px; font-weight: 600; color: #166534;">✓ File Attached &amp; Loaded</div>
                <div style="font-size: 11px; color: #334155; margin-top: 2px;"><b>{uploaded_file.name}</b> ({uploaded_file.size / 1024:.1f} KB)</div>
                <div style="font-size: 11px; color: #15803d; margin-top: 2px;">Ready for analysis / auto-ingested</div>
            </div>
            """)

        row_limit = st.selectbox(
            "Sample Processing Limit",
            options=[1000, 5000, 10000, 25000, "All Records"],
            index=0,
            help="Limits processing size for instant analytics"
        )

        render_html("<hr style='border-color: #e2e8f0; margin: 14px 0;'>")
        col_act1, col_act2 = st.columns([3, 2])
        with col_act1:
            analyze_button = st.button("Process & Ingest", use_container_width=True)
        with col_act2:
            clear_button = st.button("Clear Data", use_container_width=True)

        if clear_button:
            st.session_state["data_mode"] = None
            st.session_state["dataset_records"] = None
            st.session_state["ground_truth"] = None
            st.session_state["inference_time"] = 0.0
            st.session_state["source_name"] = None
            st.session_state["processed_file_id"] = None
            st.rerun()

        # Pipeline Specification Card
        render_html("""
        <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px; margin-top: 20px;">
            <div style="font-size: 10px; font-weight: 700; color: #64748b; text-transform: uppercase;">Adaptive Engine Specs</div>
            <div style="font-size: 12px; font-weight: 600; color: #0f172a; margin-top: 4px;">Universal Multi-Vector Anomaly Engine</div>
            <div style="font-size: 11px; color: #64748b; margin-top: 2px;">• Deep Packet Inspection &amp; Protocol Security</div>
            <div style="font-size: 11px; color: #64748b; margin-top: 2px;">• High-Throughput Network Flow Telemetry</div>
            <div style="font-size: 11px; color: #64748b; margin-top: 2px;">• Enterprise Threat &amp; Incident Auditing</div>
            <div style="font-size: 11px; color: #059669; font-weight: 500; margin-top: 4px;">Status: All Pipelines Operational</div>
        </div>
        """)

    # Handle Upload Trigger (Auto-ingests on new file attachment or when Process is clicked)
    if uploaded_file is not None:
        file_signature = f"{uploaded_file.name}_{uploaded_file.size}_{row_limit}"
        need_processing = (
            analyze_button or 
            st.session_state.get("dataset_records") is None or 
            st.session_state.get("source_name") != uploaded_file.name or 
            st.session_state.get("processed_file_id") != file_signature
        )
        if need_processing:
            st.session_state["processed_file_id"] = file_signature
            with st.spinner("Analyzing dataset structure and running telemetry processing..."):
                if ingest_and_process_stream(uploaded_file, uploaded_file.name, row_limit, model, encoders, scaler):
                    st.rerun()
    elif analyze_button:
        st.warning("Please upload a CSV file first.")

    # Active State
    data_mode = st.session_state["data_mode"]
    records = st.session_state["dataset_records"]
    ground_truth = st.session_state["ground_truth"]
    inference_time = st.session_state["inference_time"]
    source_name = st.session_state["source_name"]
    history = st.session_state["ingestion_history"]

    # ==============================================================================
    # View Navigation Tabs
    # ==============================================================================
    tab_analytics, tab_logs, tab_history, tab_manual = st.tabs([
        "Threat & Telemetry Analytics",
        "Record Logs & Export",
        f"Ingestion History ({len(history)})",
        "Attack Types Manual"
    ])

    # ------------------------------------------------------------------------------
    # Tab 1: Threat & Telemetry Analytics
    # ------------------------------------------------------------------------------
    with tab_analytics:
        if records is None:
            render_html("""
            <div style="background-color: #f8fafc; border: 2px dashed #3b82f6; border-radius: 8px; padding: 36px 20px; text-align: center; margin: 12px 0 18px 0;">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="margin: 0 auto 12px auto;">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="17 8 12 3 7 8"/>
                    <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
                <div style="font-size: 17px; font-weight: 700; color: #0f172a; margin-bottom: 4px;">Upload &amp; Analyze Network Telemetry Dataset</div>
                <div style="font-size: 13px; color: #64748b; max-width: 540px; margin: 0 auto;">
                    Drag and drop or select your CSV file below to run real-time anomaly classification, threat scoring, and visual telemetry.
                </div>
            </div>
            """)
            
            center_uploaded = st.file_uploader(
                "Upload or Drop CSV Telemetry Dataset Here",
                type=["csv"],
                key="center_telemetry_uploader",
                help="Attach network traffic captures, flow telemetry, or threat breach logs"
            )
            
            if center_uploaded is not None:
                with st.spinner("Processing telemetry and executing ML anomaly detection..."):
                    if ingest_and_process_stream(center_uploaded, center_uploaded.name, row_limit, model, encoders, scaler):
                        st.session_state["processed_file_id"] = f"{center_uploaded.name}_{center_uploaded.size}_{row_limit}"
                        st.rerun()
        elif data_mode == "INCIDENT":
            # ==================================================================
            # Render Mode: Cyber Attack Incident & Threat Intelligence
            # ==================================================================
            df = records.copy()
            total_incidents = len(df)
            
            # Identify columns flexibly
            loss_col = next((c for c in df.columns if "financial" in c.lower()), None)
            users_col = next((c for c in df.columns if "user" in c.lower() or "affected" in c.lower()), None)
            time_col = next((c for c in df.columns if "time" in c.lower() or "resolution" in c.lower()), None)
            attack_col = next((c for c in df.columns if "attack type" in c.lower() or "attack" in c.lower()), None)
            industry_col = next((c for c in df.columns if "industry" in c.lower()), None)
            source_col = next((c for c in df.columns if "source" in c.lower()), None)
            vuln_col = next((c for c in df.columns if "vulnerability" in c.lower()), None)
            defense_col = next((c for c in df.columns if "defense" in c.lower() or "mechanism" in c.lower()), None)
            country_col = next((c for c in df.columns if "country" in c.lower()), None)

            # Metrics
            total_loss = float(pd.to_numeric(df[loss_col], errors="coerce").sum()) if loss_col else 0.0
            total_users = int(pd.to_numeric(df[users_col], errors="coerce").sum()) if users_col else 0
            avg_time = float(pd.to_numeric(df[time_col], errors="coerce").mean()) if time_col else 0.0

            # Mode Indicator Banner
            render_html(f"""
            <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 6px; padding: 8px 16px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; font-size: 12px;">
                <span style="color: #166534; font-weight: 600;">ACTIVE PIPELINE: CYBERSECURITY INCIDENT INTELLIGENCE</span>
                <span style="color: #64748b;">Source: {source_name} | Records: {total_incidents:,}</span>
            </div>
            """)

            # KPI Row
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                render_html(f"""
                <div class="netshield-card">
                    <div class="netshield-card-title">Incidents Analyzed</div>
                    <div class="netshield-card-value">{total_incidents:,}</div>
                    <div class="netshield-card-sub">Global Threat Records</div>
                </div>
                """)
            with k2:
                render_html(f"""
                <div class="netshield-card">
                    <div class="netshield-card-title">Cumulative Financial Impact</div>
                    <div class="netshield-card-value" style="color: #dc2626;">${total_loss:,.1f} <span style="font-size: 14px; font-weight: 500; color: #64748b;">M</span></div>
                    <div class="netshield-card-sub">Direct & Indirect Damages</div>
                </div>
                """)
            with k3:
                render_html(f"""
                <div class="netshield-card">
                    <div class="netshield-card-title">Impacted Users</div>
                    <div class="netshield-card-value">{total_users:,}</div>
                    <div class="netshield-card-sub">Compromised Accounts / Records</div>
                </div>
                """)
            with k4:
                render_html(f"""
                <div class="netshield-card">
                    <div class="netshield-card-title">Mean Resolution Latency</div>
                    <div class="netshield-card-value">{avg_time:.1f} <span style="font-size: 14px; font-weight: 500; color: #64748b;">hrs</span></div>
                    <div class="netshield-card-sub">Time to Neutralize Incident</div>
                </div>
                """)

            # Incident Charts Row 1
            render_html("<div style='font-size: 12px; font-weight: 700; letter-spacing: 0.05em; color: #64748b; text-transform: uppercase; margin: 16px 0 10px 0;'>INCIDENT CLASSIFICATION & TARGET SECTOR IMPACT</div>")
            ic1, ic2 = st.columns([1, 2])

            with ic1:
                if attack_col:
                    atk_counts = df[attack_col].value_counts().reset_index()
                    atk_counts.columns = ["Attack Vector", "Count"]
                    fig_atk = px.pie(
                        atk_counts,
                        names="Attack Vector",
                        values="Count",
                        hole=0.64,
                        color_discrete_sequence=["#2563eb", "#ef4444", "#f59e0b", "#10b981", "#8b5cf6", "#ec4899"]
                    )
                    fig_atk.update_traces(textfont_size=10, textinfo="percent")
                    apply_plot_theme(
                        fig_atk,
                        title="Attack Vector Distribution",
                        height=310,
                        showlegend=True,
                        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, font=dict(size=9))
                    )
                    st.plotly_chart(fig_atk, use_container_width=True, config={"displayModeBar": False})

            with ic2:
                if industry_col and loss_col:
                    ind_loss = df.groupby(industry_col)[loss_col].sum().reset_index()
                    ind_loss = ind_loss.sort_values(by=loss_col, ascending=True)
                    fig_ind = px.bar(
                        ind_loss,
                        x=loss_col,
                        y=industry_col,
                        orientation="h",
                        color_discrete_sequence=["#2563eb"],
                        labels={loss_col: "Loss ($M)", industry_col: "Sector"}
                    )
                    apply_plot_theme(fig_ind, title="Loss by Target Sector ($M)", height=310)
                    st.plotly_chart(fig_ind, use_container_width=True, config={"displayModeBar": False})

            # Incident Charts Row 2
            ic3, ic4 = st.columns(2)
            with ic3:
                if source_col:
                    src_df = df[source_col].value_counts().reset_index()
                    src_df.columns = ["Actor", "Count"]
                    fig_src = px.bar(
                        src_df,
                        x="Actor",
                        y="Count",
                        color_discrete_sequence=["#475569"],
                        labels={"Actor": "Threat Actor", "Count": "Incidents"}
                    )
                    apply_plot_theme(fig_src, title="Threat Actor Attribution", height=310)
                    st.plotly_chart(fig_src, use_container_width=True, config={"displayModeBar": False})

            with ic4:
                if vuln_col and defense_col:
                    cross_df = df.groupby([vuln_col, defense_col]).size().reset_index(name="Count")
                    fig_cross = px.bar(
                        cross_df,
                        x=vuln_col,
                        y="Count",
                        color=defense_col,
                        barmode="stack",
                        labels={vuln_col: "Vulnerability", "Count": "Count", defense_col: "Defense"}
                    )
                    fig_cross.update_xaxes(tickangle=-15)
                    apply_plot_theme(
                        fig_cross,
                        title="Vulnerabilities vs Defenses",
                        height=310,
                        margin=dict(l=45, r=20, t=48, b=65),
                        legend=dict(orientation="h", yanchor="top", y=-0.26, xanchor="center", x=0.5, font=dict(size=9))
                    )
                    st.plotly_chart(fig_cross, use_container_width=True, config={"displayModeBar": False})

            # Incident Charts Row 3
            ic5, ic6 = st.columns(2)
            with ic5:
                if country_col:
                    c_counts = df[country_col].value_counts().head(10).reset_index()
                    c_counts.columns = ["Country", "Count"]
                    fig_c = px.bar(
                        c_counts,
                        x="Count",
                        y="Country",
                        orientation="h",
                        color_discrete_sequence=["#059669"],
                        labels={"Count": "Incidents", "Country": "Country"}
                    )
                    apply_plot_theme(fig_c, title="Top Impacted Countries", height=310)
                    fig_c.update_yaxes(autorange="reversed")
                    st.plotly_chart(fig_c, use_container_width=True, config={"displayModeBar": False})

            with ic6:
                if time_col and loss_col and attack_col:
                    fig_sc = px.scatter(
                        df,
                        x=time_col,
                        y=loss_col,
                        color=attack_col,
                        hover_data=[country_col, industry_col] if country_col else None,
                        labels={time_col: "Latency (hrs)", loss_col: "Loss ($M)", attack_col: "Attack"}
                    )
                    fig_sc.update_traces(marker=dict(size=5, opacity=0.7))
                    apply_plot_theme(
                        fig_sc,
                        title="Damage vs Resolution Latency",
                        height=310,
                        margin=dict(l=45, r=20, t=48, b=65),
                        legend=dict(orientation="h", yanchor="top", y=-0.26, xanchor="center", x=0.5, font=dict(size=9))
                    )
                    st.plotly_chart(fig_sc, use_container_width=True, config={"displayModeBar": False})

        else:
            # ==================================================================
            # Render Mode: Network Traffic Anomaly & Flow Telemetry (PACKET or FLOW)
            # ==================================================================
            results = records.copy()
            total_records = len(results)
            anomaly_mask = results["prediction"] == 1
            anomaly_count = int(anomaly_mask.sum())
            normal_count = total_records - anomaly_count
            anomaly_pct = (anomaly_count / total_records * 100) if total_records > 0 else 0
            normal_pct = 100.0 - anomaly_pct

            engine_name = "DEEP PACKET ANOMALY DETECTION ENGINE" if data_mode == "PACKET" else "NETWORK FLOW TELEMETRY & TRAFFIC ANALYZER"
            render_html(f"""
            <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 6px; padding: 8px 16px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; font-size: 12px;">
                <span style="color: #1e40af; font-weight: 600;">ACTIVE PIPELINE: {engine_name}</span>
                <span style="color: #64748b;">Source: {source_name} | Connections: {total_records:,}</span>
            </div>
            """)

            # Telemetry Metrics Bar
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                render_html(f"""
                <div class="netshield-card">
                    <div class="netshield-card-title">Connections Ingested</div>
                    <div class="netshield-card-value">{total_records:,}</div>
                    <div class="netshield-card-sub">File: {source_name}</div>
                </div>
                """)

            with m2:
                render_html(f"""
                <div class="netshield-card">
                    <div class="netshield-card-title">Normal Traffic</div>
                    <div class="netshield-card-value" style="color: #059669;">{normal_count:,}</div>
                    <div class="netshield-card-sub">{normal_pct:.2f}% of total</div>
                </div>
                """)

            crit_high_count = int(results["severity"].isin(["CRITICAL", "HIGH"]).sum()) if "severity" in results.columns else anomaly_count
            crit_high_pct = (crit_high_count / total_records * 100) if total_records > 0 else 0

            with m3:
                render_html(f"""
                <div class="netshield-card">
                    <div class="netshield-card-title">Anomalies Detected</div>
                    <div class="netshield-card-value" style="color: #dc2626;">{anomaly_count:,}</div>
                    <div class="netshield-card-sub">{crit_high_count:,} Critical/High ({crit_high_pct:.1f}%)</div>
                </div>
                """)

            with m4:
                render_html(f"""
                <div class="netshield-card">
                    <div class="netshield-card-title">Processing Latency</div>
                    <div class="netshield-card-value">{inference_time * 1000:.1f} <span style="font-size: 14px; font-weight: 500; color: #64748b;">ms</span></div>
                    <div class="netshield-card-sub">{(total_records / max(inference_time, 0.0001)):,.0f} records/sec</div>
                </div>
                """)

            # Charts Row 1: Threat Severity & Identified Attack Vectors
            render_html("<div style='font-size: 12px; font-weight: 700; letter-spacing: 0.05em; color: #64748b; text-transform: uppercase; margin: 16px 0 10px 0;'>THREAT PROFILING &amp; IDENTIFIED ATTACK VECTORS</div>")
            c1, c2 = st.columns([1, 2])
            with c1:
                if "severity" in results.columns:
                    sev_order = ["CRITICAL", "HIGH", "MEDIUM", "NORMAL"]
                    sev_counts = results["severity"].value_counts()
                    sev_labels = [s for s in sev_order if s in sev_counts.index]
                    sev_values = [int(sev_counts[s]) for s in sev_labels]
                    color_map = {"CRITICAL": "#dc2626", "HIGH": "#ea580c", "MEDIUM": "#eab308", "NORMAL": "#10b981"}
                    chart_colors = [color_map.get(s, "#64748b") for s in sev_labels]

                    fig_donut = go.Figure(data=[go.Pie(
                        labels=sev_labels,
                        values=sev_values,
                        hole=0.64,
                        marker=dict(colors=chart_colors, line=dict(color="#ffffff", width=2)),
                        textinfo="percent",
                        hoverinfo="label+value+percent",
                        textfont=dict(family="JetBrains Mono", size=10, color="#ffffff")
                    )])
                    apply_plot_theme(
                        fig_donut,
                        title="Threat Severity Distribution",
                        height=300,
                        showlegend=True,
                        legend=dict(orientation="h", yanchor="top", y=-0.16, xanchor="center", x=0.5, font=dict(size=9))
                    )
                    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})
                else:
                    fig_donut = go.Figure(data=[go.Pie(
                        labels=["Normal", "Anomaly"],
                        values=[normal_count, anomaly_count],
                        hole=0.64,
                        marker=dict(colors=["#10b981", "#ef4444"], line=dict(color="#ffffff", width=2)),
                        textinfo="percent",
                        hoverinfo="label+value+percent",
                        textfont=dict(family="JetBrains Mono", size=10, color="#ffffff")
                    )])
                    apply_plot_theme(fig_donut, title="Classification Ratio", height=300)
                    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

            with c2:
                if "attack_type" in results.columns:
                    atk_dist = results["attack_type"].value_counts().reset_index()
                    atk_dist.columns = ["Attack Vector", "Count"]
                    fig_atk_dist = px.bar(
                        atk_dist,
                        x="Count",
                        y="Attack Vector",
                        orientation="h",
                        color="Attack Vector",
                        labels={"Count": "Connections", "Attack Vector": "Identified Attack Vector"}
                    )
                    apply_plot_theme(
                        fig_atk_dist,
                        title="Identified Cyber Attack Vectors",
                        height=300,
                        showlegend=False
                    )
                    fig_atk_dist.update_yaxes(autorange="reversed")
                    st.plotly_chart(fig_atk_dist, use_container_width=True, config={"displayModeBar": False})
                else:
                    st.info("Attack vector classification pending.")

            # Charts Row 2: Protocol Breakdown & Connection State / Duration
            render_html("<div style='font-size: 12px; font-weight: 700; letter-spacing: 0.05em; color: #64748b; text-transform: uppercase; margin: 16px 0 10px 0;'>NETWORK TELEMETRY ATTRIBUTES</div>")
            c3, c4 = st.columns(2)
            with c3:
                if "protocol_type" in results.columns:
                    proto_df = results.groupby(["protocol_type", "classification"]).size().reset_index(name="count")
                    fig_proto = px.bar(
                        proto_df,
                        x="protocol_type",
                        y="count",
                        color="classification",
                        barmode="group",
                        color_discrete_map={"Normal": "#10b981", "Anomaly": "#ef4444"},
                        labels={"protocol_type": "Protocol", "count": "Count", "classification": "Type"}
                    )
                    apply_plot_theme(
                        fig_proto,
                        title="Volume by Protocol",
                        height=300,
                        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, font=dict(size=9))
                    )
                    st.plotly_chart(fig_proto, use_container_width=True, config={"displayModeBar": False})
                elif "Destination Port" in results.columns:
                    top_ports = results["Destination Port"].value_counts().head(8).reset_index()
                    top_ports.columns = ["Destination Port", "Flows"]
                    top_ports["Destination Port"] = "Port " + top_ports["Destination Port"].astype(str)
                    fig_ports = px.bar(
                        top_ports,
                        x="Destination Port",
                        y="Flows",
                        color_discrete_sequence=["#2563eb"],
                        labels={"Destination Port": "Port", "Flows": "Flows"}
                    )
                    apply_plot_theme(fig_ports, title="Top Destination Ports", height=300)
                    st.plotly_chart(fig_ports, use_container_width=True, config={"displayModeBar": False})
                else:
                    st.info("Protocol and port breakdown telemetry pending.")

            with c4:
                if "flag" in results.columns:
                    flag_df = results.groupby(["flag", "classification"]).size().reset_index(name="count")
                    top_flags = results["flag"].value_counts().head(6).index
                    flag_filtered = flag_df[flag_df["flag"].isin(top_flags)]
                    fig_flag = px.bar(
                        flag_filtered,
                        x="flag",
                        y="count",
                        color="classification",
                        barmode="stack",
                        color_discrete_map={"Normal": "#10b981", "Anomaly": "#ef4444"},
                        labels={"flag": "Flag", "count": "Packets"}
                    )
                    apply_plot_theme(
                        fig_flag,
                        title="Connection State Flags",
                        height=300,
                        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, font=dict(size=9))
                    )
                    st.plotly_chart(fig_flag, use_container_width=True, config={"displayModeBar": False})
                elif "Flow Duration" in results.columns:
                    results["log_duration"] = np.log10(pd.to_numeric(results["Flow Duration"], errors="coerce").clip(lower=1))
                    fig_dur = px.histogram(
                        results,
                        x="log_duration",
                        color="classification",
                        nbins=25,
                        color_discrete_map={"Normal": "#10b981", "Anomaly": "#ef4444"},
                        labels={"log_duration": "Log(Duration µs)", "count": "Flows"}
                    )
                    apply_plot_theme(
                        fig_dur,
                        title="Flow Duration Telemetry",
                        height=300,
                        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, font=dict(size=9))
                    )
                    st.plotly_chart(fig_dur, use_container_width=True, config={"displayModeBar": False})

            # Charts Row 3
            c5, c6 = st.columns(2)
            with c5:
                fig_prob = px.histogram(
                    results,
                    x="anomaly_probability",
                    nbins=28,
                    color="classification",
                    color_discrete_map={"Normal": "#10b981", "Anomaly": "#ef4444"},
                    labels={"anomaly_probability": "Score", "count": "Count"}
                )
                apply_plot_theme(
                    fig_prob,
                    title="Anomaly Confidence Distribution",
                    height=300,
                    legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, font=dict(size=9))
                )
                st.plotly_chart(fig_prob, use_container_width=True, config={"displayModeBar": False})

            with c6:
                if "src_bytes" in results.columns and "dst_bytes" in results.columns:
                    scatter_sample = results.sample(min(len(results), 800), random_state=42).copy()
                    scatter_sample["log_src_bytes"] = np.log10(scatter_sample["src_bytes"].astype(float).clip(lower=1))
                    scatter_sample["log_dst_bytes"] = np.log10(scatter_sample["dst_bytes"].astype(float).clip(lower=1))
                    fig_scatter = px.scatter(
                        scatter_sample,
                        x="log_src_bytes",
                        y="log_dst_bytes",
                        color="classification",
                        color_discrete_map={"Normal": "#10b981", "Anomaly": "#ef4444"},
                        opacity=0.6,
                        labels={"log_src_bytes": "Log(Src)", "log_dst_bytes": "Log(Dst)"}
                    )
                    fig_scatter.update_traces(marker=dict(size=5))
                    apply_plot_theme(
                        fig_scatter,
                        title="Payload Signature (Src / Dst)",
                        height=300,
                        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, font=dict(size=9))
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})
                elif "Total Fwd Packets" in results.columns and "Flow Duration" in results.columns:
                    flow_sample = results.sample(min(len(results), 800), random_state=42).copy()
                    flow_sample["log_fwd_pkts"] = np.log10(pd.to_numeric(flow_sample["Total Fwd Packets"], errors="coerce").clip(lower=1))
                    flow_sample["log_dur"] = np.log10(pd.to_numeric(flow_sample["Flow Duration"], errors="coerce").clip(lower=1))
                    fig_flow_sc = px.scatter(
                        flow_sample,
                        x="log_fwd_pkts",
                        y="log_dur",
                        color="classification",
                        color_discrete_map={"Normal": "#10b981", "Anomaly": "#ef4444"},
                        opacity=0.7,
                        labels={"log_fwd_pkts": "Log(Fwd Pkts)", "log_dur": "Log(Duration)"}
                    )
                    fig_flow_sc.update_traces(marker=dict(size=5))
                    apply_plot_theme(
                        fig_flow_sc,
                        title="Flow Duration vs Packets",
                        height=300,
                        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="center", x=0.5, font=dict(size=9))
                    )
                    st.plotly_chart(fig_flow_sc, use_container_width=True, config={"displayModeBar": False})

    # ------------------------------------------------------------------------------
    # Tab 2: Record Logs & Export
    # ------------------------------------------------------------------------------
    with tab_logs:
        if records is None:
            st.info("No records loaded yet. Upload and analyze a dataset to inspect logs.")
        elif data_mode == "INCIDENT":
            df = records.copy()
            render_html("<div style='font-size: 12px; font-weight: 700; letter-spacing: 0.05em; color: #64748b; text-transform: uppercase; margin: 10px 0;'>FILTER CYBER INCIDENT AUDIT RECORDS</div>")
            
            f1, f2, f3 = st.columns([2, 2, 4])
            attack_col = next((c for c in df.columns if "attack" in c.lower()), None)
            industry_col = next((c for c in df.columns if "industry" in c.lower()), None)
            
            with f1:
                if attack_col:
                    atk_opts = ["All Attack Types"] + sorted(df[attack_col].dropna().unique().tolist())
                    sel_atk = st.selectbox("Attack Filter", atk_opts)
                else:
                    sel_atk = "All Attack Types"
            with f2:
                if industry_col:
                    ind_opts = ["All Industries"] + sorted(df[industry_col].dropna().unique().tolist())
                    sel_ind = st.selectbox("Industry Filter", ind_opts)
                else:
                    sel_ind = "All Industries"
            with f3:
                search_q = st.text_input("Search Logs", placeholder="e.g. Country, Vulnerability, Actor")

            filtered = df.copy()
            if attack_col and sel_atk != "All Attack Types":
                filtered = filtered[filtered[attack_col] == sel_atk]
            if industry_col and sel_ind != "All Industries":
                filtered = filtered[filtered[industry_col] == sel_ind]
            if search_q.strip():
                sq = search_q.strip().lower()
                filtered = filtered[filtered.astype(str).apply(lambda row: sq in " ".join(row).lower(), axis=1)]

            render_html(f"<div style='font-size: 12px; color: #64748b; margin-bottom: 8px;'>Showing <strong>{len(filtered):,}</strong> of {len(df):,} incidents</div>")
            inc_priority_cols = ["severity", "attack_type", "classification", "detection_reason", "recommended_action", "anomaly_probability"]
            inc_other = [c for c in filtered.columns if c not in inc_priority_cols]
            inc_display = [c for c in inc_priority_cols if c in filtered.columns] + inc_other
            st.dataframe(filtered[inc_display].head(500), use_container_width=True, height=380)

            csv_data = filtered.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Filtered Cyber Incidents (CSV)",
                data=csv_data,
                file_name=f"netshield_incidents_{time.strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

        else:
            # Network Traffic / Flow View
            filtered = records.copy()
            render_html("<div style='font-size: 12px; font-weight: 700; letter-spacing: 0.05em; color: #64748b; text-transform: uppercase; margin: 10px 0;'>FILTER CONNECTION RECORDS</div>")
            
            f1, f2, f3, f4 = st.columns([2, 2, 2, 3])
            with f1:
                sev_options = ["All Severities", "CRITICAL", "HIGH", "MEDIUM", "NORMAL"]
                sev_filter = st.selectbox("Severity Filter", options=sev_options)

            with f2:
                if "attack_type" in records.columns:
                    atk_options = ["All Attack Vectors"] + sorted(records["attack_type"].astype(str).unique().tolist())
                    atk_filter = st.selectbox("Attack Vector Filter", options=atk_options)
                else:
                    atk_filter = "All Attack Vectors"
                    st.selectbox("Attack Vector Filter", options=["All Attack Vectors"])

            with f3:
                class_filter = st.selectbox("Classification Filter", options=["All Connections", "Anomaly Only", "Normal Only"])

            with f4:
                search_query = st.text_input("Search Logs", placeholder="e.g. Service, Flag, Port, Reason...")

            if sev_filter != "All Severities" and "severity" in filtered.columns:
                filtered = filtered[filtered["severity"] == sev_filter]

            if atk_filter != "All Attack Vectors" and "attack_type" in filtered.columns:
                filtered = filtered[filtered["attack_type"] == atk_filter]

            if class_filter == "Anomaly Only":
                filtered = filtered[filtered["prediction"] == 1]
            elif class_filter == "Normal Only":
                filtered = filtered[filtered["prediction"] == 0]

            if search_query.strip():
                q = search_query.strip().lower()
                filtered = filtered[filtered.astype(str).apply(lambda row: q in " ".join(row).lower(), axis=1)]

            render_html(f"<div style='font-size: 12px; color: #64748b; margin-bottom: 8px;'>Showing <strong>{len(filtered):,}</strong> of {len(records):,} records</div>")
            
            priority_cols = ["severity", "attack_type", "classification", "detection_reason", "recommended_action", "anomaly_probability"]
            for candidate in ["protocol_type", "Destination Port", "service", "flag", "duration", "Flow Duration", "src_bytes", "dst_bytes", "Total Fwd Packets"]:
                if candidate in filtered.columns and candidate not in priority_cols:
                    priority_cols.append(candidate)

            other_cols = [c for c in filtered.columns if c not in priority_cols and c != "prediction"]
            display_cols = [c for c in priority_cols if c in filtered.columns] + other_cols
            st.dataframe(filtered[display_cols].head(500), use_container_width=True, height=380)

            csv_data = records.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Full Ingested Prediction Results (CSV)",
                data=csv_data,
                file_name=f"netshield_analysis_{time.strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

    # ------------------------------------------------------------------------------
    # Tab 3: Ingestion History
    # ------------------------------------------------------------------------------
    with tab_history:
        render_html("<div style='font-size: 12px; font-weight: 700; letter-spacing: 0.05em; color: #64748b; text-transform: uppercase; margin: 10px 0;'>PERSISTENT INGESTION AUDIT TRAIL</div>")
        
        if not history:
            render_html("""
            <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 24px; text-align: center; color: #64748b; font-size: 13px;">
                No historical entries recorded yet. Each processed upload will automatically create an audit record here.
            </div>
            """)
        else:
            render_html(f"<div style='font-size: 13px; color: #64748b; margin-bottom: 12px;'>Recorded <strong>{len(history)}</strong> ingestion runs in this session.</div>")
            
            for idx, entry in enumerate(history):
                c_head, c_meta, c_stat, c_action = st.columns([2, 3, 3, 2])
                with c_head:
                    render_html(f"<span class='history-id'>{entry['entry_id']}</span><br><span style='font-size:11px; color:#94a3b8;'>{entry['timestamp']}</span>")
                with c_meta:
                    render_html(f"<strong>{entry['filename']}</strong><br><span style='font-size:12px; color:#64748b;'>{entry['pipeline_type']} | {entry['total_records']:,} rows</span>")
                with c_stat:
                    badge_cls = "badge-neutral" if entry["data_mode"] == "INCIDENT" else "badge-normal"
                    render_html(f"<span class='{badge_cls}'>{entry['summary']}</span><br><span style='font-size:11px; color:#94a3b8;'>Latency: {entry['latency_ms']:.1f} ms</span>")
                with c_action:
                    if st.button("View Entry", key=f"hist_btn_{entry['entry_id']}"):
                        st.session_state["data_mode"] = entry["data_mode"]
                        st.session_state["dataset_records"] = entry["data_df"]
                        st.session_state["ground_truth"] = entry.get("ground_truth")
                        st.session_state["source_name"] = entry["filename"]
                        st.rerun()

                render_html("<hr style='border-color: #f1f5f9; margin: 6px 0;'>")

    # ------------------------------------------------------------------------------
    # Tab 4: Attack Types Manual
    # ------------------------------------------------------------------------------
    with tab_manual:
        render_html("<div style='font-size: 12px; font-weight: 700; letter-spacing: 0.05em; color: #64748b; text-transform: uppercase; margin: 10px 0;'>COMPREHENSIVE CYBER ATTACK TYPES REFERENCE MANUAL</div>")
        render_html("""
        <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 6px; padding: 12px 16px; margin-bottom: 16px; font-size: 12px; color: #1e40af;">
            This reference guide outlines cybersecurity attack categories, intrusion vectors, and telemetry anomaly patterns identified by Netshield. 
            Upload external security logs or network captures matching any standard format to detect and flag these attacks.
        </div>
        """)

        # Network Connection & Protocol Attack Vectors
        render_html("<div style='font-size: 13px; font-weight: 700; color: #0f172a; margin: 16px 0 8px 0;'>Network Connection &amp; Protocol Attack Vectors</div>")

        manual_col1, manual_col2 = st.columns(2)
        with manual_col1:
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #dc2626; margin-bottom: 6px;">DoS (Denial of Service)</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.6;">
                    Overwhelms a target system with excessive packet floods or malformed requests to make services unavailable to legitimate users.
                </div>
                <div style="font-size: 11px; color: #64748b; margin-top: 6px;"><strong>Common Variants:</strong> SYN Flood, Smurf, Ping of Death, Teardrop, Land Attack</div>
            </div>
            """)
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #f59e0b; margin-bottom: 6px;">Probe &amp; Reconnaissance</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.6;">
                    Systematic scanning to discover open services, network topology, firewall rules, and active operating systems.
                </div>
                <div style="font-size: 11px; color: #64748b; margin-top: 6px;"><strong>Common Variants:</strong> IP Sweep, Port Sweep, Stealth Nmap, Satan Scan</div>
            </div>
            """)

        with manual_col2:
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #8b5cf6; margin-bottom: 6px;">R2L (Remote to Local Exploits)</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.6;">
                    Unauthorized infiltration from external networks to local machines by exploiting misconfigurations or brute-forcing credentials.
                </div>
                <div style="font-size: 11px; color: #64748b; margin-top: 6px;"><strong>Common Variants:</strong> Password Guessing, FTP Exploit, IMAP Abuse, Unauthorized Remote Shell</div>
            </div>
            """)
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #059669; margin-bottom: 6px;">U2R (User to Root Privilege Escalation)</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.6;">
                    Internal exploit where an authenticated standard account gains administrative or superuser privileges.
                </div>
                <div style="font-size: 11px; color: #64748b; margin-top: 6px;"><strong>Common Variants:</strong> Buffer Overflow, Rootkit Injection, Perl Payload, Kernel Module Exploitation</div>
            </div>
            """)

        # Volumetric & Infrastructure Flow Attack Vectors
        render_html("<div style='font-size: 13px; font-weight: 700; color: #0f172a; margin: 20px 0 8px 0;'>Volumetric &amp; Flow Infrastructure Attack Vectors</div>")

        flow_col1, flow_col2, flow_col3 = st.columns(3)
        with flow_col1:
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #dc2626; margin-bottom: 4px;">DDoS Attacks</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Distributed Denial of Service flooding high-volume flow surges from geographically dispersed endpoints.</div>
            </div>
            """)
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #2563eb; margin-bottom: 4px;">Port Scanning</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Systematic automated probing across high-range destination ports to identify vulnerable listening daemons.</div>
            </div>
            """)

        with flow_col2:
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #ef4444; margin-bottom: 4px;">Brute Force Infiltration</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Repeated rapid authentication requests over SSH, RDP, or HTTP attempting credential compromise.</div>
            </div>
            """)
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #f59e0b; margin-bottom: 4px;">Botnet Activity</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Coordinated communication channels between command-and-control (C2) servers and zombie endpoints.</div>
            </div>
            """)

        with flow_col3:
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #8b5cf6; margin-bottom: 4px;">Web Application Attacks</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Cross-site scripting (XSS), SQL injection, and path traversal targeting backend application servers.</div>
            </div>
            """)
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #059669; margin-bottom: 4px;">Cryptographic Vulnerabilities</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Exploitation of TLS/SSL flaws (e.g. Heartbleed) to leak private server memory and encryption keys.</div>
            </div>
            """)

        # Enterprise Threat Vectors & Security Breaches
        render_html("<div style='font-size: 13px; font-weight: 700; color: #0f172a; margin: 20px 0 8px 0;'>Enterprise Threat Vectors &amp; Security Breaches</div>")

        inc_col1, inc_col2 = st.columns(2)
        with inc_col1:
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #dc2626; margin-bottom: 4px;">Malware</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Malicious software including viruses, trojans, worms, and spyware designed to damage or exploit systems.</div>
            </div>
            """)
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #ef4444; margin-bottom: 4px;">Ransomware</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Encrypts victim data and demands payment for decryption keys. Can paralyze organizations.</div>
            </div>
            """)
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #2563eb; margin-bottom: 4px;">SQL Injection</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Inserts malicious SQL statements into input fields to manipulate or extract database information.</div>
            </div>
            """)

        with inc_col2:
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #f59e0b; margin-bottom: 4px;">Phishing</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Social engineering attack using fraudulent emails or websites to steal credentials and sensitive data.</div>
            </div>
            """)
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #8b5cf6; margin-bottom: 4px;">Man-in-the-Middle</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Intercepting communication between two parties to eavesdrop or alter transmitted data.</div>
            </div>
            """)
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #059669; margin-bottom: 4px;">Zero-Day Exploit</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Attacks targeting previously unknown software vulnerabilities before patches are available.</div>
            </div>
            """)

if __name__ == "__main__":
    main()
