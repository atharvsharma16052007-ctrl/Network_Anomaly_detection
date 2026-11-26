import os
import sys
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_styled_deck(output_path="NETSHIELD_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Modern Swiss/Editorial Theme Palette
    C_BG = RGBColor(255, 255, 255)         # Pure White
    C_CARD_BG = RGBColor(248, 250, 252)    # Slate Light (#F8FAFC)
    C_BORDER = RGBColor(226, 232, 240)     # Clean Border (#E2E8F0)
    C_DARK = RGBColor(15, 23, 42)          # Deep Slate (#0F172A)
    C_MUTED = RGBColor(100, 116, 139)      # Slate Muted (#64748B)
    C_PRIMARY = RGBColor(37, 99, 235)      # Royal Cobalt (#2563EB)
    C_EMERALD = RGBColor(5, 150, 105)      # Forest Emerald (#059669)
    C_CRIMSON = RGBColor(220, 38, 38)      # Crimson Red (#DC2626)
    C_ORANGE = RGBColor(234, 88, 12)       # Amber (#EA580C)
    C_WHITE = RGBColor(255, 255, 255)

    blank_layout = prs.slide_layouts[6]

    def set_white_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def add_top_tracker(slide, slide_num, total_slides=10):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.35))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"NETSHIELD  /  SYSTEM ARCHITECTURE & ML PIPELINE    {slide_num:02d} / {total_slides:02d}"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = C_PRIMARY

    def add_slide_header(slide, main_title, subtitle=""):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.733), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = main_title
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        
        if subtitle:
            p2 = tf.add_paragraph()
            p2.text = subtitle
            p2.font.size = Pt(11)
            p2.font.color.rgb = C_MUTED
            p2.space_before = Pt(3)

    def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    def add_badge(slide, left, top, text, bg_color=C_DARK, txt_color=C_WHITE, w=Inches(0.42), h=Inches(0.28)):
        badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, w, h)
        badge.fill.solid()
        badge.fill.fore_color.rgb = bg_color
        badge.line.fill.background()
        tf = badge.text_frame
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = txt_color
        p.alignment = PP_ALIGN.CENTER
        return badge

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_white_bg(s1)

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "SMART INDIA HACKATHON // CYBER DEFENSE INITIATIVE"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.733), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "NETSHIELD"
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    
    p = tf.add_paragraph()
    p.text = "AI-Driven Network Traffic Anomaly & Threat Detection System"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p.space_before = Pt(4)

    p = tf.add_paragraph()
    p.text = "A high-throughput machine learning pipeline and explainable decision framework that transforms raw, unlabeled network traffic into actionable security intelligence."
    p.font.size = Pt(12)
    p.font.color.rgb = C_MUTED
    p.space_before = Pt(8)

    # 4 Key Highlights Cards
    kpis = [
        ("Two-Stage Architecture", "ML Anomaly Screening + Explainable Threat Profiler"),
        ("100 Trees Random Forest", "Bootstrap ensemble with zero data leakage"),
        ("~260,000 Records/Sec", "Sub-4ms line-rate inference on standard CPUs"),
        ("Decision-Ready Output", "Attack Vector + Severity Level + Mitigation Action")
    ]
    c_w = Inches(2.78)
    for i, (title, desc) in enumerate(kpis):
        x = Inches(0.8) + i * Inches(2.98)
        add_card(s1, x, Inches(4.3), c_w, Inches(2.3))
        add_badge(s1, x + Inches(0.2), Inches(4.55), f"0{i+1}", C_PRIMARY)
        
        tb = s1.shapes.add_textbox(x + Inches(0.2), Inches(5.0), c_w - Inches(0.4), Inches(1.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 2: THE PROBLEM STATEMENT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_white_bg(s2)
    add_top_tracker(s2, 2)
    add_slide_header(s2, "The Core Problem: Why Static Rules Fail & What AI Solves",
                     "Traditional firewalls miss novel traffic patterns; standard ML flags anomalies without explaining what went wrong.")

    cols = [
        ("Traditional Rule-Based Firewalls", C_CRIMSON, [
            ("Static Signature Matching", "Matches incoming packets only against a pre-compiled library of known threats."),
            ("Blind to Novel Attacks", "Fails completely when traffic patterns change or attackers alter techniques."),
            ("High Administrative Burden", "Requires continuous manual intervention and constant rule updates.")
        ]),
        ("Standard Black-Box Machine Learning", C_ORANGE, [
            ("Statistical Pattern Deviation", "Detects unexpected traffic shifts, but outputs only a binary 0 or 1 flag."),
            ("The '0 vs 1' Output Trap", "Alerts administrators that traffic is abnormal, but gives zero explanation of the cause."),
            ("Paralyzes Triage Response", "Operators cannot decide whether to rate-limit traffic, block an IP, or isolate a machine.")
        ]),
        ("The Netshield Solution: Two-Stage AI", C_PRIMARY, [
            ("Stage 1: High-Speed ML Screening", "Ensemble Random Forest screens 100% of network traffic at ~260,000 records/sec."),
            ("Stage 2: Explainable Threat Profiling", "Deterministic profiler maps pattern signatures into human-readable attack types."),
            ("Actionable Defense Decision", "Outputs an immediate Severity Rating (Critical to Normal) and prescriptive mitigation step.")
        ])
    ]

    for i, (title, accent, points) in enumerate(cols):
        x = Inches(0.8) + i * Inches(4.0)
        card = add_card(s2, x, Inches(1.85), Inches(3.8), Inches(4.9))
        
        # Color accent line on top of card
        top_bar = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.85), Inches(3.8), Inches(0.08))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = accent
        top_bar.line.fill.background()

        add_badge(s2, x + Inches(0.25), Inches(2.1), f"0{i+1}", accent)

        tb = s2.shapes.add_textbox(x + Inches(0.25), Inches(2.6), Inches(3.3), Inches(4.0))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        for heading, body in points:
            p = tf.add_paragraph()
            p.text = f"• {heading}"
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.color.rgb = C_DARK
            p.space_before = Pt(10)
            
            p = tf.add_paragraph()
            p.text = body
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_MUTED
            p.space_before = Pt(2)

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_white_bg(s3)
    add_top_tracker(s3, 3)
    add_slide_header(s3, "System Architecture: End-to-End 5-Stage AI Pipeline",
                     "Decoupled pipeline separating fast statistical screening from transparent, explainable threat attribution.")

    steps = [
        ("01", "Data Ingestion", "Dynamic intake of network capture CSV files with zero preloaded data."),
        ("02", "Feature Preprocessing", "Automated feature alignment, label encoding, and StandardScaler Z-score normalization."),
        ("03", "Stage-1 ML Model", "Parallel Random Forest ensemble (100 trees) outputting anomaly probability scores."),
        ("04", "Stage-2 Threat Profiler", "Multi-factor heuristic mapping anomaly attributes to concrete threat categories & severity."),
        ("05", "Interactive SOC Dashboard", "Plotly visual analytics, tabular audit logs, and one-click data export.")
    ]

    card_w = Inches(2.23)
    for i, (num, title, desc) in enumerate(steps):
        x = Inches(0.8) + i * Inches(2.38)
        add_card(s3, x, Inches(1.85), card_w, Inches(3.4))
        add_badge(s3, x + Inches(0.2), Inches(2.05), num, C_PRIMARY)

        tb = s3.shapes.add_textbox(x + Inches(0.2), Inches(2.55), card_w - Inches(0.4), Inches(2.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(8)

    # Architectural Rationale Box
    add_card(s3, Inches(0.8), Inches(5.5), Inches(11.733), Inches(1.4), C_CARD_BG, C_BORDER)
    tb = s3.shapes.add_textbox(Inches(1.1), Inches(5.65), Inches(11.133), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ARCHITECTURAL BENEFIT: DECOUPLING DETECTION FROM PROFILING"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    p = tf.add_paragraph()
    p.text = "Decoupling statistical anomaly detection (Stage 1) from deterministic threat profiling (Stage 2) achieves sub-4ms line-rate inference throughput while maintaining transparent, 100% auditable reasoning that network operators and security auditors can verify."
    p.font.size = Pt(10)
    p.font.color.rgb = C_DARK
    p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 4: MULTI-SCHEMA INGESTION
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_white_bg(s4)
    add_top_tracker(s4, 4)
    add_slide_header(s4, "Multi-Schema Ingestion: Adapting to Any Network Telemetry Stream",
                     "Automated schema detection normalizes diverse telemetry formats into a consistent tensor structure.")

    schemas = [
        ("Packet-Level Network Telemetry", C_PRIMARY, [
            "41 connection features: protocol type, service, TCP flags, duration, and byte volume.",
            "Evaluates individual connection sessions between network hosts.",
            "Detects half-open connection errors, scanning patterns, and access anomalies."
        ]),
        ("Network Flow Telemetry", C_EMERALD, [
            "Aggregated traffic flow statistics: duration, packet counts, and byte rates.",
            "Monitors high-throughput core network switches and gateway routers.",
            "Identifies volumetric traffic surges, packet floods, and abnormal destination ports."
        ]),
        ("Enterprise Incident Logs", C_DARK, [
            "Historical cybersecurity incident records: attack types, affected assets, and loss metrics.",
            "Used for post-incident audit reporting, impact assessment, and trend forecasting.",
            "Integrates historical breach intelligence with real-time operational defense."
        ])
    ]

    for i, (title, color, bullets) in enumerate(schemas):
        x = Inches(0.8) + i * Inches(4.0)
        add_card(s4, x, Inches(1.85), Inches(3.8), Inches(3.4))
        add_badge(s4, x + Inches(0.25), Inches(2.1), f"0{i+1}", color)

        tb = s4.shapes.add_textbox(x + Inches(0.25), Inches(2.6), Inches(3.3), Inches(2.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_MUTED
            p.space_before = Pt(6)

    # Ingestion Lifecycle Workflow Box
    add_card(s4, Inches(0.8), Inches(5.5), Inches(11.733), Inches(1.4), C_CARD_BG, C_BORDER)
    tb = s4.shapes.add_textbox(Inches(1.1), Inches(5.65), Inches(11.133), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "THE 4-STEP INGESTION LIFECYCLE"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    p = tf.add_paragraph()
    p.text = "1. Data Intake (Drag & Drop CSV) ──▶ 2. Automatic Schema Discovery ──▶ 3. Zero-Leakage Preprocessing & Normalization ──▶ 4. Parallel ML Batch Inference"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 5: PREPROCESSING & FEATURE PIPELINE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_white_bg(s5)
    add_top_tracker(s5, 5)
    add_slide_header(s5, "Data Preprocessing: Strict Data Contract & Zero-Leakage Pipeline",
                     "Transforms raw, heterogeneous network attributes into normalized float32 tensors with mathematical guarantees.")

    feat_groups = [
        ("Connection Basics", "duration, src_bytes, dst_bytes", "StandardScaler (Z-Score)", "Normalizes extreme byte variance while preserving traffic distribution."),
        ("System Indicators", "num_failed_logins, root_shell, is_guest", "Binary & MinMax", "Preserves exact 0/1 indicators for unauthorized access attempts."),
        ("Traffic Error Rates", "count, serror_rate, rerror_rate", "StandardScaler", "Normalizes connection frequencies and error ratios across time windows."),
        ("Categorical Flags", "protocol_type, service, flag", "Deterministic Encoding", "Maps categorical strings to integers with dedicated unseen token handling.")
    ]

    card_w = Inches(2.78)
    for i, (group, examples, transform, purpose) in enumerate(feat_groups):
        x = Inches(0.8) + i * Inches(2.98)
        add_card(s5, x, Inches(1.85), card_w, Inches(3.4))
        add_badge(s5, x + Inches(0.2), Inches(2.05), f"F{i+1}", C_PRIMARY)

        tb = s5.shapes.add_textbox(x + Inches(0.2), Inches(2.5), card_w - Inches(0.4), Inches(2.6))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = group
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        p = tf.add_paragraph()
        p.text = f"Fields: {examples}"
        p.font.size = Pt(9)
        p.font.color.rgb = C_PRIMARY
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = f"Method: {transform}"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = purpose
        p.font.size = Pt(9)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(6)

    # Mathematical Guarantees
    add_card(s5, Inches(0.8), Inches(5.5), Inches(11.733), Inches(1.4), C_CARD_BG, C_BORDER)
    tb = s5.shapes.add_textbox(Inches(1.1), Inches(5.65), Inches(11.133), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ZERO DATA LEAKAGE GUARANTEE"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    p = tf.add_paragraph()
    p.text = "All StandardScaler transforms and categorical encoders are strictly fitted on the training split (80%) only. The held-out test split (20%) is exclusively transformed without learning new statistical parameters, preventing statistical contamination and optimistic bias."
    p.font.size = Pt(10)
    p.font.color.rgb = C_DARK
    p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 6: MACHINE LEARNING MODEL ARCHITECTURE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_white_bg(s6)
    add_top_tracker(s6, 6)
    add_slide_header(s6, "Machine Learning Architecture: Random Forest Classifier",
                     "Supervised ensemble combining 100 decision trees for robust, non-linear anomaly classification.")

    # Left Card: Why Random Forest
    add_card(s6, Inches(0.8), Inches(1.85), Inches(6.8), Inches(5.0))
    tb = s6.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(6.2), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "WHY RANDOM FOREST OVER DEEP LEARNING?"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    reasons = [
        ("Tabular Superiority", "Decision tree ensembles consistently outperform deep neural networks on structured network telemetry featuring heterogeneous numerical and categorical columns."),
        ("Zero GPU Infrastructure Required", "Executes sub-4ms line-rate inference on commodity enterprise CPUs without requiring costly GPU acceleration."),
        ("Ensemble Generalization", "Bootstrap aggregation (bagging) across 100 decorrelated trees averages out individual variance and prevents overfitting on traffic bursts."),
        ("Calibrated Probability Output", "Outputs a smooth, continuous anomaly confidence score P(anomaly) between 0.00 and 1.00 rather than an arbitrary binary guess.")
    ]

    for title, desc in reasons:
        p = tf.add_paragraph()
        p.text = f"• {title}:"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_before = Pt(8)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(2)

    # Right Card: Specifications Table
    add_card(s6, Inches(7.8), Inches(1.85), Inches(4.733), Inches(5.0))
    tb = s6.shapes.add_textbox(Inches(8.1), Inches(2.1), Inches(4.133), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "MODEL CONFIGURATION SPECIFICATIONS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    specs = [
        ("Ensemble Estimators", "100 Decision Trees"),
        ("Splitting Criterion", "Gini Impurity / Entropy"),
        ("Decision Boundary", "tau = 0.50 (Calibrated)"),
        ("Parallel Execution", "Threaded (n_jobs = -1)"),
        ("Artifact Footprint", "6.84 MB (Compact)"),
        ("Operational Memory", "~18 MB RAM"),
        ("Batch Inference Speed", "3.79 ms / 1,000 records")
    ]

    for label, val in specs:
        p = tf.add_paragraph()
        p.text = f"{label}:"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = val
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_before = Pt(1)

    # =========================================================================
    # SLIDE 7: TWO-STAGE THREAT ENGINE & PROFILER
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_white_bg(s7)
    add_top_tracker(s7, 7)
    add_slide_header(s7, "Two-Stage Threat Profiler: From Statistical Score to Plain English",
                     "Transforms opaque machine learning predictions into human-readable attack types and containment playbooks.")

    categories = [
        ("Denial of Service (DoS)", "CRITICAL", C_CRIMSON, 
         "Traffic floods designed to overwhelm network bandwidth and service capacity.",
         "High error rate + connection spikes",
         "Enable rate limiting & drop source IP"),
        
        ("System Infiltration & Exploits", "CRITICAL", C_CRIMSON,
         "Attempts to hijack administrative access or execute unauthorized system commands.",
         "Abnormal root/admin indicators",
         "Immediately isolate affected host"),
        
        ("Reconnaissance & Scanning", "HIGH", C_ORANGE,
         "Systematic probing across multiple ports and services to find open vulnerabilities.",
         "High destination service variation",
         "Block scanning subnet at edge firewall"),
        
        ("Unauthorized Access Attempts", "MEDIUM", C_PRIMARY,
         "Repeated password guessing and failed remote authentication requests.",
         "Multiple failed login attempts",
         "Enforce multi-factor auth & lock account")
    ]

    c_w = Inches(2.78)
    for i, (cat, sev, color, desc, trigger, action) in enumerate(categories):
        x = Inches(0.8) + i * Inches(2.98)
        add_card(s7, x, Inches(1.85), c_w, Inches(3.4))
        add_badge(s7, x + Inches(0.2), Inches(2.05), sev, color, C_WHITE, Inches(0.8), Inches(0.26))

        tb = s7.shapes.add_textbox(x + Inches(0.2), Inches(2.45), c_w - Inches(0.4), Inches(2.6))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = cat
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = f"Trigger: {trigger}"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_before = Pt(6)

        p = tf.add_paragraph()
        p.text = f"Action: {action}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = color
        p.space_before = Pt(3)

    # Output Contract Banner
    add_card(s7, Inches(0.8), Inches(5.5), Inches(11.733), Inches(1.4), C_CARD_BG, C_BORDER)
    tb = s7.shapes.add_textbox(Inches(1.1), Inches(5.65), Inches(11.133), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "EXPLAINABLE ALERT OUTPUT CONTRACT"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    p = tf.add_paragraph()
    p.text = "[ Attack Category ]  +  [ Severity Rating ]  +  [ Plain-English Trigger Reason ]  +  [ Actionable Mitigation ]"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p.space_before = Pt(4)

    p = tf.add_paragraph()
    p.text = "Eliminates operator hesitation by giving triage engineers the exact context and remediation command needed to stop threats."
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_MUTED
    p.space_before = Pt(2)

    # =========================================================================
    # SLIDE 8: TRAINING SETUP & EVALUATION METHODOLOGY
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_white_bg(s8)
    add_top_tracker(s8, 8)
    add_slide_header(s8, "Training Setup & Validation Strategy",
                     "Rigorous 80/20 train-test partitioning with complete statistical isolation to prevent data contamination.")

    # Left Card: Partitioning Breakdown
    add_card(s8, Inches(0.8), Inches(1.85), Inches(5.7), Inches(5.0))
    tb = s8.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(5.1), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "DATASET PARTITIONING & SCALE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    parts = [
        ("Total Telemetry Records", "125,974 connection sessions across all standard protocol types."),
        ("Training Set (80%)", "100,779 records used exclusively for feature fitting and tree ensemble training."),
        ("Held-out Test Set (20%)", "25,195 records strictly held out for final generalization testing."),
        ("Stratified Class Balance", "Maintains exact proportion of benign and anomalous sessions in both training and test sets.")
    ]

    for title, desc in parts:
        p = tf.add_paragraph()
        p.text = f"• {title}:"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_before = Pt(8)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(2)

    # Right Card: Validation Safeguards
    add_card(s8, Inches(6.8), Inches(1.85), Inches(5.733), Inches(5.0))
    tb = s8.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.133), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ENGINEERING SAFEGUARDS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    safeguards = [
        ("Preprocessing Isolation", "Encoders and scalers are fitted strictly on the 80% train split. Test data is never visible to feature scaling."),
        ("Cost-Sensitive Optimization", "Penalizes false negatives during leaf splitting to prioritize catching high-risk intrusions."),
        ("Unseen Protocol Handling", "Unknown or mutated protocol tokens encountered during evaluation are safely mapped to a dedicated fallback index."),
        ("Deterministic Reproducibility", "Fixed pseudo-random seed ensures identical model weights and repeatable benchmark results.")
    ]

    for title, desc in safeguards:
        p = tf.add_paragraph()
        p.text = f"• {title}:"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_before = Pt(8)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(2)

    # =========================================================================
    # SLIDE 9: MEASURED PERFORMANCE & BENCHMARKS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_white_bg(s9)
    add_top_tracker(s9, 9)
    add_slide_header(s9, "Measured Performance: Validated on 25,195 Unseen Test Records",
                     "Empirical validation confirms near-perfect accuracy combined with line-rate processing throughput.")

    metrics = [
        ("99.90%", "ACCURACY", "Correct classification across all test records", C_PRIMARY),
        ("99.83%", "RECALL", "Catches 998+ of every 1,000 malicious connections", C_EMERALD),
        ("99.89%", "F1-SCORE", "Harmonic balance between precision and recall", C_PRIMARY),
        ("0.04%", "FALSE POSITIVE", "Only ~4 false alerts per 10,000 normal sessions", C_DARK)
    ]

    c_w = Inches(2.78)
    for i, (val, label, sub, color) in enumerate(metrics):
        x = Inches(0.8) + i * Inches(2.98)
        add_card(s9, x, Inches(1.85), c_w, Inches(2.5))
        
        tb = s9.shapes.add_textbox(x + Inches(0.15), Inches(2.05), c_w - Inches(0.3), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = val
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = color
        
        p = tf.add_paragraph()
        p.text = label
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = sub
        p.font.size = Pt(9)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(4)

    # Inference Throughput Benchmark Card
    add_card(s9, Inches(0.8), Inches(4.6), Inches(11.733), Inches(2.3), C_CARD_BG, C_BORDER)
    tb = s9.shapes.add_textbox(Inches(1.1), Inches(4.8), Inches(11.133), Inches(1.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "LINE-RATE THROUGHPUT & INFERENCE LATENCY BENCHMARK"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    benchmarks = [
        ("Inference Speed: 3.79 ms / 1,000 records", "Evaluates a batch of 1,000 connections in under 4 milliseconds on standard CPU cores."),
        ("Line-Rate Throughput: 263,806 records / second", "Processes over 260K connections per second, easily supporting high-speed network gateways."),
        ("Full Test Evaluation: 95.5 ms for 25,195 records", "Evaluates the entire 25,195 test split in less than a tenth of a second.")
    ]

    for title, desc in benchmarks:
        p = tf.add_paragraph()
        p.text = f"• {title} — {desc}"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 10: CONCLUSION & ACHIEVEMENTS (NO FUTURE SCOPE!)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_white_bg(s10)
    add_top_tracker(s10, 10)
    add_slide_header(s10, "Project Summary & Core Technical Deliverables",
                     "A production-ready AI anomaly detection prototype delivering speed, precision, and explainability.")

    deliverables = [
        ("01", "Fully Implemented End-to-End Pipeline",
         "Built a complete AI-driven pipeline handling raw data intake, automated feature normalization, ensemble model scoring, and visual reporting."),
        
        ("02", "Solved the Black-Box Dilemma",
         "The Two-Stage Engine replaces cryptic numeric flags with human-readable attack types, severity ratings, and prescriptive mitigation actions."),
        
        ("03", "Extreme Line-Rate Throughput",
         "Achieved 263,800+ records/sec at 99.90% accuracy with sub-4ms batch latency on commodity CPU hardware without requiring GPUs."),
        
        ("04", "Dual Deployment Readiness",
         "Delivered both a local interactive console (localhost:8501) and a client-side web deployment ready for immediate live demonstration.")
    ]

    card_w = Inches(2.78)
    for i, (num, title, desc) in enumerate(deliverables):
        x = Inches(0.8) + i * Inches(2.98)
        add_card(s10, x, Inches(1.85), card_w, Inches(3.4))
        add_badge(s10, x + Inches(0.2), Inches(2.05), num, C_PRIMARY)

        tb = s10.shapes.add_textbox(x + Inches(0.2), Inches(2.5), card_w - Inches(0.4), Inches(2.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(8)

    # Key Takeaways Box (Replacing Future Scope)
    add_card(s10, Inches(0.8), Inches(5.5), Inches(11.733), Inches(1.4), C_CARD_BG, C_BORDER)
    tb = s10.shapes.add_textbox(Inches(1.1), Inches(5.65), Inches(11.133), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CORE PROJECT IMPACT & VALUE PROPOSITION"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    p = tf.add_paragraph()
    p.text = "Netshield proves that machine learning can deliver both high statistical precision and operational explainability in network monitoring. By translating statistical anomaly patterns into immediate, actionable defense steps, it bridges the gap between AI detection and effective incident response."
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p.space_before = Pt(4)

    prs.save(output_path)
    print(f"Styled presentation generated successfully: {output_path}")

if __name__ == "__main__":
    out = "NETSHIELD_Presentation.pptx"
    if len(sys.argv) > 1:
        out = sys.argv[1]
    build_styled_deck(out)
