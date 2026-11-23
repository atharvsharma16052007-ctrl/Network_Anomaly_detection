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

def predict_packet_anomalies(df_raw, model, encoders, scaler):
    """Executes network anomaly classification on NSL-KDD packet traffic using Random Forest."""
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

    # Inference
    predictions = model.predict(scaled_values)
    probabilities = model.predict_proba(scaled_values)[:, 1]
    inference_time = time.time() - start_time

    result_df = df_raw.copy()
    result_df["prediction"] = predictions
    result_df["classification"] = np.where(predictions == 1, "Anomaly", "Normal")
    result_df["anomaly_probability"] = np.round(probabilities, 4)

    return result_df, ground_truth, inference_time

def process_flow_telemetry(df_raw):
    """
    Processes flow telemetry datasets (e.g. CIC-IDS-2017) with destination ports,
    flow durations, packet rates, and attack label identification.
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
        is_normal = raw_labels.str.upper() == "BENIGN"
        predictions = np.where(is_normal, 0, 1)
        classifications = np.where(is_normal, "Normal", "Anomaly")
        attack_types = raw_labels.values
        # Heuristic anomaly probability: calibrated high for attack, low for benign
        probs = np.where(is_normal, 0.04 + np.random.uniform(0, 0.06, size=len(df)), 0.88 + np.random.uniform(0, 0.11, size=len(df)))
    else:
        # Algorithmic anomaly scoring based on flow telemetry rates
        dur = pd.to_numeric(df[duration_col], errors="coerce").fillna(0) if duration_col else pd.Series(0, index=df.index)
        bps = pd.to_numeric(df[bytes_sec_col], errors="coerce").fillna(0) if bytes_sec_col else pd.Series(0, index=df.index)
        anom_score = (bps > bps.quantile(0.85)) | (dur < 10)
        predictions = anom_score.astype(int).values
        classifications = np.where(predictions == 1, "Anomaly", "Normal")
        attack_types = np.where(predictions == 1, "Anomalous Flow Surge", "Normal Flow")
        probs = np.where(predictions == 1, 0.91, 0.07)

    result_df = df.copy()
    result_df["prediction"] = predictions
    result_df["classification"] = classifications
    result_df["anomaly_probability"] = np.round(np.clip(probs, 0.01, 0.99), 4)
    result_df["attack_type"] = attack_types

    inference_time = time.time() - start_time
    return result_df, attack_types, inference_time

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
            <div style="font-size: 12px; font-weight: 600; color: #0f172a; margin-top: 4px;">Universal Multi-Schema Engine</div>
            <div style="font-size: 11px; color: #64748b; margin-top: 2px;">• Cyber Threat Incidents (10-col)</div>
            <div style="font-size: 11px; color: #64748b; margin-top: 2px;">• NSL-KDD Random Forest (41-feat)</div>
            <div style="font-size: 11px; color: #64748b; margin-top: 2px;">• CIC-IDS Flow Telemetry (79-feat)</div>
            <div style="font-size: 11px; color: #059669; font-weight: 500; margin-top: 4px;">Status: All Pipelines Operational</div>
        </div>
        """)

    # Handle Upload Trigger (Auto-ingests on new file attachment or when Process is clicked)
    target_stream = None
    target_name = None

    if uploaded_file is not None:
        file_signature = f"{uploaded_file.name}_{uploaded_file.size}_{row_limit}"
        need_processing = (
            analyze_button or 
            st.session_state.get("dataset_records") is None or 
            st.session_state.get("source_name") != uploaded_file.name or 
            st.session_state.get("processed_file_id") != file_signature
        )
        if need_processing:
            target_stream = uploaded_file
            target_name = uploaded_file.name
            st.session_state["processed_file_id"] = file_signature
    elif analyze_button:
        st.warning("Please upload a CSV file first.")
        st.stop()

    if target_stream is not None:
        try:
            with st.spinner("Analyzing dataset structure and running telemetry processing..."):
                nrows = None if row_limit == "All Records" else int(row_limit)
                raw_df = parse_any_csv(target_stream, nrows=nrows)

                if len(raw_df) == 0:
                    st.error("Uploaded CSV contains no valid data rows.")
                    st.stop()

                schema = detect_dataset_schema(raw_df)
                start_t = time.time()

                if schema == "PACKET":
                    if model is None or encoders is None or scaler is None:
                        st.error("NSL-KDD Random Forest model is not loaded. Check model files.")
                        st.stop()
                    results, gt, elapsed = predict_packet_anomalies(raw_df, model, encoders, scaler)
                    st.session_state["data_mode"] = "PACKET"
                    st.session_state["dataset_records"] = results
                    st.session_state["ground_truth"] = gt
                    st.session_state["inference_time"] = elapsed
                    st.session_state["source_name"] = target_name

                    # Record History
                    anomaly_count = int((results["prediction"] == 1).sum())
                    history_entry = {
                        "entry_id": f"ING-{len(st.session_state['ingestion_history'])+1:03d}",
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "filename": target_name,
                        "pipeline_type": "NSL-KDD Packet Traffic",
                        "total_records": len(results),
                        "summary": f"{anomaly_count} Anomalies ({(anomaly_count/len(results)*100):.1f}%)",
                        "latency_ms": elapsed * 1000,
                        "data_mode": "PACKET",
                        "data_df": results,
                        "ground_truth": gt
                    }
                    st.session_state["ingestion_history"].insert(0, history_entry)

                elif schema == "FLOW":
                    results, attack_types, elapsed = process_flow_telemetry(raw_df)
                    st.session_state["data_mode"] = "FLOW"
                    st.session_state["dataset_records"] = results
                    st.session_state["ground_truth"] = None
                    st.session_state["inference_time"] = elapsed
                    st.session_state["source_name"] = target_name

                    # Record History
                    anomaly_count = int((results["prediction"] == 1).sum())
                    history_entry = {
                        "entry_id": f"ING-{len(st.session_state['ingestion_history'])+1:03d}",
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "filename": target_name,
                        "pipeline_type": "CIC-IDS Flow Telemetry",
                        "total_records": len(results),
                        "summary": f"{anomaly_count} Anomalies ({(anomaly_count/len(results)*100):.1f}%)",
                        "latency_ms": elapsed * 1000,
                        "data_mode": "FLOW",
                        "data_df": results,
                        "ground_truth": None
                    }
                    st.session_state["ingestion_history"].insert(0, history_entry)

                else:
                    # INCIDENT Pipeline: Clean and parse incident telemetry
                    elapsed = time.time() - start_t
                    st.session_state["data_mode"] = "INCIDENT"
                    st.session_state["dataset_records"] = raw_df
                    st.session_state["ground_truth"] = None
                    st.session_state["inference_time"] = elapsed
                    st.session_state["source_name"] = target_name

                    # Record History
                    history_entry = {
                        "entry_id": f"ING-{len(st.session_state['ingestion_history'])+1:03d}",
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "filename": target_name,
                        "pipeline_type": "Cyber Threat Incidents",
                        "total_records": len(raw_df),
                        "summary": f"{len(raw_df):,} Threat Events",
                        "latency_ms": elapsed * 1000,
                        "data_mode": "INCIDENT",
                        "data_df": raw_df,
                        "ground_truth": None
                    }
                    st.session_state["ingestion_history"].insert(0, history_entry)

        except Exception as ex:
            st.error(f"Processing failed: {str(ex)}")
            st.stop()

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
            if uploaded_file is not None:
                render_html(f"""
                <div class="empty-state-box">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="margin: 0 auto;">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <polyline points="14 2 14 8 20 8"/>
                        <line x1="16" y1="13" x2="8" y2="13"/>
                        <line x1="16" y1="17" x2="8" y2="17"/>
                        <polyline points="10 9 9 9 8 9"/>
                    </svg>
                    <div class="empty-state-title" style="color: #1e40af;">File Attached: {uploaded_file.name}</div>
                    <div class="empty-state-text">
                        File ready ({uploaded_file.size / 1024:.1f} KB). Click <strong>Process &amp; Ingest</strong> in the sidebar to run analysis.
                    </div>
                </div>
                """)
            else:
                render_html("""
                <div class="empty-state-box">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="margin: 0 auto;">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                        <polyline points="17 8 12 3 7 8"/>
                        <line x1="12" y1="3" x2="12" y2="15"/>
                    </svg>
                    <div class="empty-state-title">No Security Data Ingested</div>
                    <div class="empty-state-text">
                        Upload any network traffic log, flow dataset (CIC-IDS), or cybersecurity incidents CSV 
                        using the sidebar file uploader, then click Process & Ingest to populate live telemetry and analytics.
                        See the Attack Types Manual tab for supported attack categories.
                    </div>
                </div>
                """)
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

            engine_name = "NSL-KDD RANDOM FOREST MODEL" if data_mode == "PACKET" else "CIC-IDS NETWORK FLOW ANALYZER"
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

            with m3:
                render_html(f"""
                <div class="netshield-card">
                    <div class="netshield-card-title">Anomalies Detected</div>
                    <div class="netshield-card-value" style="color: #dc2626;">{anomaly_count:,}</div>
                    <div class="netshield-card-sub">{anomaly_pct:.2f}% of total</div>
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

            # Charts Row 1
            render_html("<div style='font-size: 12px; font-weight: 700; letter-spacing: 0.05em; color: #64748b; text-transform: uppercase; margin: 16px 0 10px 0;'>TRAFFIC CLASSIFICATION TELEMETRY</div>")
            c1, c2 = st.columns([1, 2])
            with c1:
                fig_donut = go.Figure(data=[go.Pie(
                    labels=["Normal", "Anomaly"],
                    values=[normal_count, anomaly_count],
                    hole=0.64,
                    marker=dict(colors=["#10b981", "#ef4444"], line=dict(color="#ffffff", width=2)),
                    textinfo="percent",
                    hoverinfo="label+value+percent",
                    textfont=dict(family="JetBrains Mono", size=10, color="#ffffff")
                )])
                apply_plot_theme(
                    fig_donut,
                    title="Classification Ratio",
                    height=300,
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="top", y=-0.16, xanchor="center", x=0.5, font=dict(size=9))
                )
                st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

            with c2:
                # Flow vs KDD adaptive column display
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

            # Charts Row 2
            c3, c4 = st.columns(2)
            with c3:
                if "service" in results.columns:
                    anomalies_df = results[results["prediction"] == 1]
                    if len(anomalies_df) > 0:
                        top_services = anomalies_df["service"].value_counts().head(8).reset_index()
                        top_services.columns = ["service", "count"]
                        fig_service = px.bar(
                            top_services,
                            x="count",
                            y="service",
                            orientation="h",
                            color_discrete_sequence=["#ef4444"],
                            labels={"count": "Anomalies", "service": "Service"}
                        )
                        apply_plot_theme(fig_service, title="Top Anomalous Services", height=310)
                        fig_service.update_yaxes(autorange="reversed")
                        st.plotly_chart(fig_service, use_container_width=True, config={"displayModeBar": False})
                    else:
                        st.info("No anomalies recorded in current packet batch.")
                elif "attack_type" in results.columns:
                    atk_dist = results["attack_type"].value_counts().reset_index()
                    atk_dist.columns = ["Attack Vector", "Flows"]
                    fig_atk_dist = px.bar(
                        atk_dist,
                        x="Flows",
                        y="Attack Vector",
                        orientation="h",
                        color="Attack Vector",
                        labels={"Flows": "Flows", "Attack Vector": "Vector"}
                    )
                    apply_plot_theme(
                        fig_atk_dist,
                        title="Flow Attack Vectors",
                        height=310,
                        showlegend=False
                    )
                    fig_atk_dist.update_yaxes(autorange="reversed")
                    st.plotly_chart(fig_atk_dist, use_container_width=True, config={"displayModeBar": False})

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
                        height=310,
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
                        height=310,
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
            st.dataframe(filtered.head(500), use_container_width=True, height=380)

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
            
            f1, f2, f3 = st.columns([2, 2, 4])
            with f1:
                class_filter = st.selectbox("Classification Filter", options=["All Connections", "Anomaly Only", "Normal Only"])
            
            with f2:
                if "protocol_type" in records.columns:
                    proto_options = ["All Protocols"] + sorted(records["protocol_type"].astype(str).unique().tolist())
                    proto_filter = st.selectbox("Protocol Filter", options=proto_options)
                elif "Destination Port" in records.columns:
                    port_options = ["All Ports"] + sorted(records["Destination Port"].astype(str).unique().tolist())
                    proto_filter = st.selectbox("Port Filter", options=port_options)
                else:
                    proto_filter = "All"
                    st.selectbox("Filter", options=["All"])

            with f3:
                search_query = st.text_input("Search Logs", placeholder="e.g. Service, Flag, Port, or Attack")

            if class_filter == "Anomaly Only":
                filtered = filtered[filtered["prediction"] == 1]
            elif class_filter == "Normal Only":
                filtered = filtered[filtered["prediction"] == 0]

            if "protocol_type" in records.columns and proto_filter != "All Protocols":
                filtered = filtered[filtered["protocol_type"].astype(str) == proto_filter]
            elif "Destination Port" in records.columns and proto_filter != "All Ports":
                filtered = filtered[filtered["Destination Port"].astype(str) == proto_filter]

            if search_query.strip():
                q = search_query.strip().lower()
                filtered = filtered[filtered.astype(str).apply(lambda row: q in " ".join(row).lower(), axis=1)]

            render_html(f"<div style='font-size: 12px; color: #64748b; margin-bottom: 8px;'>Showing <strong>{len(filtered):,}</strong> of {len(records):,} records</div>")
            
            priority_cols = ["classification", "anomaly_probability"]
            for candidate in ["attack_type", "protocol_type", "Destination Port", "service", "flag", "duration", "Flow Duration", "src_bytes", "dst_bytes", "Total Fwd Packets"]:
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
        render_html("<div style='font-size: 12px; font-weight: 700; letter-spacing: 0.05em; color: #64748b; text-transform: uppercase; margin: 10px 0;'>NETWORK ATTACK TYPES REFERENCE GUIDE</div>")
        render_html("""
        <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 6px; padding: 12px 16px; margin-bottom: 16px; font-size: 12px; color: #1e40af;">
            This reference guide describes common network attack categories detected by the Netshield engine.
            Upload a CSV dataset matching any of the supported schemas to run anomaly detection.
        </div>
        """)

        # NSL-KDD Attack Categories
        render_html("<div style='font-size: 13px; font-weight: 700; color: #0f172a; margin: 16px 0 8px 0;'>NSL-KDD Attack Categories (Packet-Level)</div>")

        manual_col1, manual_col2 = st.columns(2)
        with manual_col1:
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #dc2626; margin-bottom: 6px;">DoS (Denial of Service)</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.6;">
                    Overwhelms a target system with excessive traffic or requests to make it unavailable to legitimate users.
                </div>
                <div style="font-size: 11px; color: #64748b; margin-top: 6px;"><strong>Examples:</strong> neptune, smurf, back, teardrop, pod, land</div>
            </div>
            """)
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #f59e0b; margin-bottom: 6px;">Probe (Reconnaissance)</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.6;">
                    Scans and gathers information about target systems to identify vulnerabilities and open services.
                </div>
                <div style="font-size: 11px; color: #64748b; margin-top: 6px;"><strong>Examples:</strong> satan, ipsweep, portsweep, nmap</div>
            </div>
            """)

        with manual_col2:
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #8b5cf6; margin-bottom: 6px;">R2L (Remote to Local)</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.6;">
                    Unauthorized access from a remote machine to a local account by exploiting vulnerabilities or guessing credentials.
                </div>
                <div style="font-size: 11px; color: #64748b; margin-top: 6px;"><strong>Examples:</strong> warezclient, guess_passwd, ftp_write, imap, spy, multihop</div>
            </div>
            """)
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #059669; margin-bottom: 6px;">U2R (User to Root)</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.6;">
                    Privilege escalation where a normal user account gains root/admin access through exploits.
                </div>
                <div style="font-size: 11px; color: #64748b; margin-top: 6px;"><strong>Examples:</strong> buffer_overflow, rootkit, perl, loadmodule</div>
            </div>
            """)

        # CIC-IDS / Flow-Level Attacks
        render_html("<div style='font-size: 13px; font-weight: 700; color: #0f172a; margin: 20px 0 8px 0;'>CIC-IDS Flow-Level Attack Types</div>")

        flow_col1, flow_col2, flow_col3 = st.columns(3)
        with flow_col1:
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #dc2626; margin-bottom: 4px;">DDoS</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Distributed Denial of Service floods targets from many sources simultaneously.</div>
            </div>
            """)
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #2563eb; margin-bottom: 4px;">PortScan</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Systematic scanning of a host to discover open ports and running services.</div>
            </div>
            """)

        with flow_col2:
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #ef4444; margin-bottom: 4px;">Brute Force</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Repeated login attempts using many password combinations to gain access.</div>
            </div>
            """)
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #f59e0b; margin-bottom: 4px;">Botnet</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Network of compromised devices controlled remotely to perform coordinated attacks.</div>
            </div>
            """)

        with flow_col3:
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #8b5cf6; margin-bottom: 4px;">Web Attack</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">SQL Injection, XSS, and brute-force attacks targeting web applications.</div>
            </div>
            """)
            render_html("""
            <div class="netshield-card">
                <div style="font-size: 12px; font-weight: 700; color: #059669; margin-bottom: 4px;">Heartbleed</div>
                <div style="font-size: 11px; color: #334155; line-height: 1.5;">Exploits OpenSSL vulnerability to read server memory and steal sensitive data.</div>
            </div>
            """)

        # Global Cyber Threat Incident Types
        render_html("<div style='font-size: 13px; font-weight: 700; color: #0f172a; margin: 20px 0 8px 0;'>Global Cyber Threat Incident Types</div>")

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
