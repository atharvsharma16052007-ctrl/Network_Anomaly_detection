import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path="NETSHIELD_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color definitions
    C_NAVY = RGBColor(15, 23, 42)       # #0f172a
    C_BLUE = RGBColor(37, 99, 235)      # #2563eb
    C_CYAN = RGBColor(14, 165, 233)     # #0ea5e9
    C_SLATE = RGBColor(71, 85, 105)     # #475569
    C_MUTED = RGBColor(148, 163, 184)   # #94a3b8
    C_LIGHT_BG = RGBColor(248, 250, 252)# #f8fafc
    C_CARD_BG = RGBColor(255, 255, 255) # #ffffff
    C_BORDER = RGBColor(226, 232, 240)  # #e2e8f0
    C_GREEN = RGBColor(16, 185, 129)    # #10b981
    C_RED = RGBColor(220, 38, 38)       # #dc2626
    C_ORANGE = RGBColor(234, 88, 12)    # #ea580c
    C_WHITE = RGBColor(255, 255, 255)

    blank_layout = prs.slide_layouts[6]

    def set_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="NETSHIELD // TECHNICAL ARCHITECTURE & DEFENSE TELEMETRY"):
        # Header banner text
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.9))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(9)
        p0.font.bold = True
        p0.font.color.rgb = C_BLUE
        
        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = C_NAVY
        p1.space_before = Pt(3)

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

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Navy Modern Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, C_NAVY)

    # Accent bar
    accent = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.08), Inches(3.6))
    accent.fill.solid()
    accent.fill.fore_color.rgb = C_CYAN
    accent.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.1), Inches(1.15), Inches(11.4), Inches(3.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "SMART INDIA HACKATHON // CYBER DEFENSE INITIATIVE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    p = tf1.add_paragraph()
    p.text = "NETSHIELD"
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.space_before = Pt(6)

    p = tf1.add_paragraph()
    p.text = "Unified Cyber Threat Telemetry & Intelligent Network Anomaly Detection System"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_before = Pt(4)

    p = tf1.add_paragraph()
    p.text = "FROM RAW PACKETS TO EXPLAINABLE THREAT INTELLIGENCE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_MUTED
    p.space_before = Pt(12)

    # Bottom Pill Badges
    badges = [
        ("Two-Stage Engine", "ML Inference + Profiler"),
        ("3 Telemetry Schemas", "Packet, Flow & Incident"),
        ("~260,000 Rec/Sec", "Sub-second Line-rate"),
        ("Explainable Alerts", "Severity + Trigger + Action")
    ]
    for i, (b_title, b_sub) in enumerate(badges):
        bx = Inches(0.8 + i * 2.95)
        by = Inches(5.3)
        add_card(s1, bx, by, Inches(2.8), Inches(1.3), bg_color=RGBColor(30, 41, 59), border_color=RGBColor(51, 65, 85))
        tb = s1.shapes.add_textbox(bx + Inches(0.15), by + Inches(0.2), Inches(2.5), Inches(0.9))
        btf = tb.text_frame
        p = btf.paragraphs[0]
        p.text = b_title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_CYAN
        p = btf.add_paragraph()
        p.text = b_sub
        p.font.size = Pt(10)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(4)

    s1.notes_slide.notes_text_frame.text = (
        "Welcome evaluators. Today we present Netshield, a production-grade cyber telemetry engine "
        "that bridges the critical operational gap between raw machine learning anomaly scoring "
        "and actionable SOC incident response. Our platform ingests packet captures, flow telemetry, "
        "and threat logs, classifying threats in sub-second latency with plain-English remediation playbooks."
    )

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT (The SOC Dilemma)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, C_LIGHT_BG)
    add_header(s2, "Binary Detection Is Not Response: The SOC Operations Gap")

    cols = [
        ("Traditional Signature NIDS", C_SLATE, [
            ("Precise on Known Signatures", "Zero ambiguity for previously cataloged attacks like static CVEs."),
            ("Blind to Zero-Days & Mutations", "Fails as soon as attackers tweak payloads, ports, or evasion wrappers."),
            ("Static Output Only", "Outputs a cryptic rule ID without behavioral anomaly context.")
        ]),
        ("Standard Black-Box ML", C_RED, [
            ("Detects Novel Anomaly Patterns", "Statistical baselines spot unexpected traffic deviations."),
            ("The '0 vs 1' Output Trap", "Flags 'Anomaly' without explaining which attack vector triggered it."),
            ("Paralyzes SOC Analysts", "Triage teams cannot tell whether to block port 22, deploy SYN cookies, or isolate roots.")
        ]),
        ("Netshield Dual-Stage Solution", C_BLUE, [
            ("High-Throughput ML Screening", "Sub-4ms screening separating benign baseline from intrusions."),
            ("Deterministic Stage-2 Profiler", "Maps error rates, TCP flags, and bytes to concrete threat vectors."),
            ("Decision-Ready Output", "Instant Severity badge (CRITICAL to NORMAL), plain-English cause, and containment playbook.")
        ])
    ]

    for i, (title, header_col, items) in enumerate(cols):
        cx = Inches(0.8 + i * 3.95)
        add_card(s2, cx, Inches(1.5), Inches(3.8), Inches(4.5))
        
        # Header bar in card
        hbar = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(1.5), Inches(3.8), Inches(0.6))
        hbar.fill.solid()
        hbar.fill.fore_color.rgb = header_col
        hbar.line.fill.background()
        
        htf = hbar.text_frame
        hp = htf.paragraphs[0]
        hp.text = title
        hp.font.size = Pt(12)
        hp.font.bold = True
        hp.font.color.rgb = C_WHITE
        hp.alignment = PP_ALIGN.CENTER
        
        tb = s2.shapes.add_textbox(cx + Inches(0.2), Inches(2.25), Inches(3.4), Inches(3.6))
        ctf = tb.text_frame
        ctf.word_wrap = True
        for j, (head, body) in enumerate(items):
            p = ctf.add_paragraph() if j > 0 else ctf.paragraphs[0]
            p.text = f"• {head}"
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = C_NAVY
            p.space_before = Pt(8) if j > 0 else Pt(0)
            
            p2 = ctf.add_paragraph()
            p2.text = body
            p2.font.size = Pt(10)
            p2.font.color.rgb = C_SLATE
            p2.space_before = Pt(2)

    # Scope banner at bottom
    add_card(s2, Inches(0.8), Inches(6.2), Inches(11.733), Inches(0.8), bg_color=RGBColor(239, 246, 255), border_color=RGBColor(191, 219, 254))
    sb_tb = s2.shapes.add_textbox(Inches(1.0), Inches(6.25), Inches(11.3), Inches(0.7))
    stf = sb_tb.text_frame
    p = stf.paragraphs[0]
    p.text = "OPERATIONAL SCOPE: Network connection screening & telemetry threat profiling. Host-level endpoint kernel memory forensics are delegated to EDR agents."
    p.font.size = Pt(10)
    p.font.color.rgb = C_BLUE
    p.font.bold = True

    s2.notes_slide.notes_text_frame.text = (
        "In enterprise Security Operations Centers, analysts don't just need to know IF something is anomalous. "
        "They must know WHAT it is, HOW critical it is, and WHAT to do right now. Raw ML models fail here because "
        "they only output a binary 0 or 1. Netshield solves this by coupling fast ML screening with an explainable "
        "threat signature profiler."
    )

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, C_LIGHT_BG)
    add_header(s3, "System Architecture: Five Stages from Telemetry to Defense")

    stages = [
        ("01", "Capture & Ingest", "Universal CSV parsing, packet captures & continuous flow streams"),
        ("02", "Adaptive Normalizer", "Auto-schema detection, zero-leakage scaling & deterministic encoding"),
        ("03", "Stage-1 ML Model", "Parallelized Random Forest ensemble generating calibrated anomaly probability"),
        ("04", "Stage-2 Profiler", "Multi-factor threat profiling mapping signatures to attack vectors & severity"),
        ("05", "SOC Action Console", "Plotly visualization, telemetry logs, persistent audit trails & export")
    ]

    for i, (num, name, desc) in enumerate(stages):
        cx = Inches(0.8 + i * 2.37)
        add_card(s3, cx, Inches(1.6), Inches(2.25), Inches(3.3))
        
        # Badge
        badge = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx + Inches(0.2), Inches(1.8), Inches(0.6), Inches(0.35))
        badge.fill.solid()
        badge.fill.fore_color.rgb = C_BLUE
        badge.line.fill.background()
        btf = badge.text_frame
        bp = btf.paragraphs[0]
        bp.text = num
        bp.font.size = Pt(11)
        bp.font.bold = True
        bp.font.color.rgb = C_WHITE
        bp.alignment = PP_ALIGN.CENTER
        
        tb = s3.shapes.add_textbox(cx + Inches(0.2), Inches(2.3), Inches(1.85), Inches(2.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = name
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.space_before = Pt(4)
        
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = C_SLATE
        p.space_before = Pt(8)

    # Architectural Rationale Cards
    add_card(s3, Inches(0.8), Inches(5.1), Inches(5.7), Inches(1.8))
    tb = s3.shapes.add_textbox(Inches(1.0), Inches(5.2), Inches(5.3), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "WHY THE TWO-STAGE SEPARATION?"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p = tf.add_paragraph()
    p.text = "Decoupling statistical anomaly detection from deterministic threat profiling ensures microsecond line-rate screening while maintaining transparent, auditable decision trees that SOC engineers can legally and operationally verify."
    p.font.size = Pt(10)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(4)

    add_card(s3, Inches(6.8), Inches(5.1), Inches(5.733), Inches(1.8))
    tb = s3.shapes.add_textbox(Inches(7.0), Inches(5.2), Inches(5.3), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PRODUCTION TECH STACK"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p = tf.add_paragraph()
    p.text = "• Core Inference: scikit-learn optimized Random Forest, Joblib memory mapping\n• Preprocessing: NumPy vectorization, StandardScaler & Robust Encoders\n• Console / UI: Streamlit, Tailwind responsive styling & Plotly telemetry charts"
    p.font.size = Pt(10)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(4)

    s3.notes_slide.notes_text_frame.text = (
        "Here is the high-level architecture. Notice how data flows unidirectionally from ingestion through normalization, "
        "fast ML inference, signature profiling, and finally into the SOC console. This separation guarantees both "
        "extreme line-rate speed and explainable output."
    )

    # =========================================================================
    # SLIDE 4: MULTI-INPUT INGESTION
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, C_LIGHT_BG)
    add_header(s4, "Multi-Input Ingestion: Adapting to Any Cyber Telemetry Stream")

    schemas = [
        ("Packet-Level Telemetry", "Deep Packet Attributes", [
            "41 connection features (protocol, service, flag, durations)",
            "Byte counts, half-open error ratios, host scan rates",
            "Target: Individual TCP/UDP/ICMP connection sessions"
        ]),
        ("Flow Telemetry Captures", "NetFlow / IPFIX Telemetry", [
            "Destination port breakdown, bi-directional flow durations",
            "Packet transmission frequency and volumetric byte rates",
            "Target: High-throughput core routing and switch backbones"
        ]),
        ("Enterprise Incident Logs", "Threat Intelligence Breaches", [
            "Security vulnerability classification, target industry vectors",
            "Financial damage metrics, incident mitigation hours",
            "Target: Historical breach auditing and posture tracking"
        ])
    ]

    for i, (name, tag, pts) in enumerate(schemas):
        cx = Inches(0.8 + i * 3.95)
        add_card(s4, cx, Inches(1.5), Inches(3.8), Inches(3.4))
        tb = s4.shapes.add_textbox(cx + Inches(0.2), Inches(1.65), Inches(3.4), Inches(3.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = tag.upper()
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = C_BLUE
        p = tf.add_paragraph()
        p.text = name
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.space_before = Pt(2)
        for pt in pts:
            p = tf.add_paragraph()
            p.text = f"• {pt}"
            p.font.size = Pt(10)
            p.font.color.rgb = C_SLATE
            p.space_before = Pt(6)

    # Ingestion steps horizontal strip
    add_card(s4, Inches(0.8), Inches(5.1), Inches(11.733), Inches(1.9))
    tb = s4.shapes.add_textbox(Inches(1.0), Inches(5.2), Inches(11.3), Inches(1.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "AUTONOMIC INGESTION LIFECYCLE (6 STEPS)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    
    steps_txt = (
        "1. Stream / File Intake ──▶ Drag & drop CSV or live socket stream buffer intake.\n"
        "2. Schema Discovery   ──▶ Heuristic column signature matching detects packet vs flow vs incident schema.\n"
        "3. Normalization      ──▶ Feature alignment, StandardScaler transform and categorical encoding.\n"
        "4. ML Batch Score     ──▶ Parallel inference execution returning calibrated anomaly probabilities.\n"
        "5. Threat Profiling   ──▶ Rule-based signature evaluation assigning attack vector, severity & action.\n"
        "6. Audit Archiving    ──▶ Live ingestion history snapshot stored with latency & row counts."
    )
    p = tf.add_paragraph()
    p.text = steps_txt
    p.font.size = Pt(10)
    p.font.color.rgb = C_NAVY
    p.space_before = Pt(4)

    s4.notes_slide.notes_text_frame.text = (
        "In a real SOC environment, telemetry comes in multiple formats. Netshield does not force analysts "
        "into a rigid schema. It automatically detects whether an uploaded file is packet-level, flow-level, "
        "or threat incident data, dynamically adapting the processing pipeline."
    )

    # =========================================================================
    # SLIDE 5: DATA CONTRACT & PREPROCESSING
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5, C_LIGHT_BG)
    add_header(s5, "Data Contract: Strict Inputs & Deterministic Preprocessing")

    # Add Table
    rows, cols_cnt = 5, 4
    table_shape = s5.shapes.add_table(rows, cols_cnt, Inches(0.8), Inches(1.6), Inches(11.733), Inches(3.2))
    table = table_shape.table
    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(3.8)
    table.columns[2].width = Inches(2.6)
    table.columns[3].width = Inches(3.533)

    table_data = [
        ["Feature Group", "Included Field Examples", "Transformation Applied", "Engineering Integrity Safeguards"],
        ["Basic Connection", "duration, src_bytes, dst_bytes, wrong_fragment", "StandardScaler (Z-Score)", "Clipping negatives, log scaling for high variance byte volume"],
        ["Content & Privileges", "num_failed_logins, root_shell, su_attempted", "MinMax / Binary Float", "Preserves exact zero/one flags indicating privilege escalation"],
        ["Traffic & Error Rates", "count, serror_rate, rerror_rate, diff_srv_rate", "StandardScaler", "Continuous rates (0.0 - 1.0) normalized across window distributions"],
        ["Categorical Flags", "protocol_type, service, flag", "Deterministic LabelEncoder", "Unseen classes mapped to dedicated 'other' token; zero runtime crashes"]
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_NAVY
                p.font.bold = True
                p.font.color.rgb = C_WHITE
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_CARD_BG if r_idx % 2 == 1 else RGBColor(241, 245, 249)
                p.font.color.rgb = C_NAVY

    # Contract Highlights Cards
    add_card(s5, Inches(0.8), Inches(5.1), Inches(5.7), Inches(1.8))
    tb = s5.shapes.add_textbox(Inches(1.0), Inches(5.2), Inches(5.3), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "TENSOR PIPELINE SPECIFICATION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p = tf.add_paragraph()
    p.text = "Raw Input: (N, 41) heterogeneous tabular records\nClean Tensor: (N, 41) float32 normalized matrix\nZero Data Leakage: Scaler and Encoders fitted strictly on train split only."
    p.font.size = Pt(10)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(4)

    add_card(s5, Inches(6.8), Inches(5.1), Inches(5.733), Inches(1.8))
    tb = s5.shapes.add_textbox(Inches(7.0), Inches(5.2), Inches(5.3), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CONTRACT ENFORCEMENT & INTEGRITY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    p = tf.add_paragraph()
    p.text = "• Schema Validation: Non-conforming rows dropped or cleanly imputed\n• Defense in Depth: Unrecognized protocols do not raise unhandled exceptions\n• Reversibility: Every scaled feature can be mapped back for auditor review"
    p.font.size = Pt(10)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(4)

    s5.notes_slide.notes_text_frame.text = (
        "Our data contract is deterministic and strictly prevents data leakage. The 41 features are grouped "
        "into basic connection metrics, content privileges, traffic rates, and categoricals. Notice that unseen "
        "categories in production are safely handled without throwing runtime exceptions."
    )

    # =========================================================================
    # SLIDE 6: TWO-STAGE THREAT ENGINE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6, C_LIGHT_BG)
    add_header(s6, "Two-Stage Threat Engine: Statistical Screening + Signature Profiling")

    # Stage 1 Card
    add_card(s6, Inches(0.8), Inches(1.5), Inches(5.7), Inches(4.5))
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(4.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "STAGE 1: RANDOM FOREST ENSEMBLE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    
    st1_pts = [
        ("Architecture", "100 uncorrelated decision trees trained with bootstrap bagging."),
        ("Parallel Inference", "Threaded execution across all CPU cores (n_jobs = -1)."),
        ("Calibrated Probability", "Outputs continuous score P(anomaly) from 0.00 to 1.00."),
        ("Extreme Throughput", "Filters out 99%+ of normal traffic in single-digit milliseconds."),
        ("Decision Boundary", "Calibrated operating threshold tau = 0.50 separating benign from anomalous.")
    ]
    for h, b in st1_pts:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = b
        run.font.bold = False
        run.font.color.rgb = C_SLATE

    # Stage 2 Card
    add_card(s6, Inches(6.8), Inches(1.5), Inches(5.733), Inches(4.5))
    tb = s6.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(4.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "STAGE 2: SIGNATURE PROFILER & ENRICHMENT"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    
    st2_pts = [
        ("DoS (SYN Flood)", "CRITICAL", "High serror_rate + S0 flag; half-open handshake burst exhaustion."),
        ("U2R (Privilege Escalation)", "CRITICAL", "root_shell > 0 or su_attempted; unauthorized superuser hijacking."),
        ("R2L (Credential Exploit)", "HIGH", "num_failed_logins > 0 on FTP/Telnet; remote brute-force attack."),
        ("Probe (PortScan)", "MEDIUM", "High dst_host_diff_srv_rate + REJ flag; reconnaissance scanning."),
        ("Mitigation Playbook", "ACTION", "Automated remediation advice attached directly to each alert record.")
    ]
    for h, sev, b in st2_pts:
        p = tf.add_paragraph()
        p.text = f"• {h} [{sev}]: "
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_RED if sev == "CRITICAL" else (C_ORANGE if sev == "HIGH" else C_BLUE)
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = b
        run.font.bold = False
        run.font.color.rgb = C_SLATE

    # Output banner
    add_card(s6, Inches(0.8), Inches(6.2), Inches(11.733), Inches(0.8), bg_color=C_NAVY)
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(11.3), Inches(0.6))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "OUTPUT CONTRACT:  [ Attack Vector ]  +  [ Severity Badge ]  +  [ Plain-English Trigger ]  +  [ Mitigation Action ]"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.alignment = PP_ALIGN.CENTER

    s6.notes_slide.notes_text_frame.text = (
        "This is our key innovation: Stage 1 acts as a high-speed filter with 100 decision trees. "
        "Stage 2 then evaluates the anomalous connection's features against cybersecurity heuristics to classify "
        "whether it is a DoS SYN flood, a privilege escalation, a remote brute-force attack, or a port scan."
    )

    # =========================================================================
    # SLIDE 7: TRAINING & CONFIGURATION (BLANKS FILLED)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7, C_LIGHT_BG)
    add_header(s7, "Training & Configuration: Reproducible, Leakage-Free Setup")

    # Left Column: Data Strategy
    add_card(s7, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.5))
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(5.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "DATASET & PARTITIONING STRATEGY"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE

    items_left = [
        ("Benchmark Dataset", "Multi-Vector Enterprise Network Telemetry"),
        ("Total Records", "125,974 connection sessions across 4 attack categories"),
        ("Stratified Split", "80% Training (100,779) / 20% Held-out Test (25,195)"),
        ("Preprocessing Isolation", "StandardScaler and Encoders fitted strictly on train split"),
        ("Class Imbalance Strategy", "Stratified sampling with cost-sensitive leaf optimization"),
        ("Evaluation Partition", "Evaluated strictly on the 25,195 unseen held-out test split"),
        ("Leakage Prevention", "Zero overlap between training normalization and test evaluation")
    ]
    for h, b in items_left:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = b
        run.font.bold = False
        run.font.color.rgb = C_SLATE

    # Right Column: Hyperparameter Table
    add_card(s7, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.5))
    tb = s7.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(0.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "MODEL CONFIGURATION & SPECIFICATIONS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE

    rows, cols_cnt = 8, 2
    t_shape = s7.shapes.add_table(rows, cols_cnt, Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.5))
    t = t_shape.table
    t.columns[0].width = Inches(2.5)
    t.columns[1].width = Inches(2.8)

    hparams = [
        ("Parameter / Spec", "Active Value"),
        ("Ensemble Estimators", "100 Decision Trees"),
        ("Max Depth", "None (Pure Leaf Terminals)"),
        ("Split Criterion", "Entropy / Gini Impurity"),
        ("Feature Scaling", "StandardScaler (Z-Score)"),
        ("Artifact Disk Footprint", "6.84 MB (Ultra-Compact)"),
        ("Memory Footprint (RAM)", "~18 MB Operational RAM"),
        ("Inference Speed", "3.79 ms / 1,000-record batch")
    ]
    for r_idx, (k, v) in enumerate(hparams):
        for c_idx, val in enumerate([k, v]):
            cell = t.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_NAVY
                p.font.bold = True
                p.font.color.rgb = C_WHITE
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_CARD_BG if r_idx % 2 == 1 else RGBColor(241, 245, 249)
                p.font.color.rgb = C_NAVY
                if c_idx == 1:
                    p.font.bold = True
                    p.font.color.rgb = C_BLUE

    s7.notes_slide.notes_text_frame.text = (
        "Here are the exact training parameters: We trained on 100,779 records and evaluated on 25,195 "
        "completely unseen test records with an 80/20 stratified split. Notice the compact model footprint: "
        "only 6.84 MB on disk, allowing it to easily deploy on lightweight edge routers or micro-gateways."
    )

    # =========================================================================
    # SLIDE 8: MEASURED PERFORMANCE & BENCHMARKS (BLANKS FILLED)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8, C_LIGHT_BG)
    add_header(s8, "Measured Performance: Validated on 25,195 Unseen Test Records")

    # 4 Metric Cards
    metrics = [
        ("99.90%", "ACCURACY", "Overall classification correctness across test split", C_BLUE),
        ("99.83%", "RECALL (DETECTION)", "Catches 998+ out of every 1,000 malicious connections", C_GREEN),
        ("99.89%", "F1-SCORE", "Harmonic balance of precision (99.96%) and recall", C_BLUE),
        ("0.04%", "FALSE-POSITIVE RATE", "Only ~4 false alarms per 10,000 benign sessions", C_GREEN)
    ]
    for i, (val, title, sub, col) in enumerate(metrics):
        cx = Inches(0.8 + i * 2.95)
        add_card(s8, cx, Inches(1.5), Inches(2.8), Inches(2.0))
        tb = s8.shapes.add_textbox(cx + Inches(0.15), Inches(1.65), Inches(2.5), Inches(1.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = val
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = col
        p.alignment = PP_ALIGN.CENTER
        
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.alignment = PP_ALIGN.CENTER
        p.space_before = Pt(4)

        p = tf.add_paragraph()
        p.text = sub
        p.font.size = Pt(9)
        p.font.color.rgb = C_SLATE
        p.alignment = PP_ALIGN.CENTER
        p.space_before = Pt(2)

    # Bottom Row: Latency & Limits
    add_card(s8, Inches(0.8), Inches(3.8), Inches(5.7), Inches(3.2))
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(3.95), Inches(5.3), Inches(2.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "LATENCY & LINE-RATE THROUGHPUT BENCHMARK"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_BLUE
    
    lat_pts = [
        ("Measured Batch Latency", "95.5 ms for the entire 25,195 test split"),
        ("Per-1K Batch Speed", "3.79 ms per 1,000 connection records (beat <15ms target)"),
        ("Effective Throughput", "263,806 records/second (shatters 50K/sec target)"),
        ("Hardware Setup", "Parallel execution across 32 concurrent thread workers"),
        ("Decision Cutoff", "Calibrated decision threshold tau = 0.50")
    ]
    for h, b in lat_pts:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = b
        run.font.bold = False
        run.font.color.rgb = C_SLATE

    add_card(s8, Inches(6.8), Inches(3.8), Inches(5.733), Inches(3.2))
    tb = s8.shapes.add_textbox(Inches(7.0), Inches(3.95), Inches(5.3), Inches(2.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "HONEST OPERATIONAL LIMITATIONS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_RED
    
    lim_pts = [
        ("Domain Distribution Shifts", "Synthetic capture baselines differ from live enterprise ISP environments; periodic retraining required."),
        ("Encrypted TLS 1.3 Payloads", "Deep content inspection is blind to encrypted bytes; system relies on packet cadence, size & rate."),
        ("Novel Vector Fallback", "Unmatched anomaly signatures cleanly fall back to 'Suspicious Flow Anomaly' rather than hallucinating attack vectors.")
    ]
    for h, b in lim_pts:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = b
        run.font.bold = False
        run.font.color.rgb = C_SLATE

    s8.notes_slide.notes_text_frame.text = (
        "On the 25,195 held-out test split, Netshield achieved 99.90% accuracy, 99.83% recall, and an ultra-low "
        "false-positive rate of 0.04%. That means only 4 false alarms per 10,000 normal connections. "
        "In terms of speed, our 32-core parallel execution achieved 263,800 records per second, well beyond our target."
    )

    # =========================================================================
    # SLIDE 9: SOC ACTION CONSOLE & DASHBOARD
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9, C_LIGHT_BG)
    add_header(s9, "SOC Dashboard: From Detection to Containment")

    dashboard_cards = [
        ("Threat Severity Donut", "Real-Time Telemetry", "Interactive Plotly visualization breaking down CRITICAL, HIGH, MEDIUM & NORMAL traffic ratios."),
        ("Attack Vector Breakdown", "Vector Analytics", "Horizontal distribution bar chart classifying DoS SYN floods, PortScans, Brute-Force and privilege escalation."),
        ("Dual Ingestion Dropzones", "Seamless Data Intake", "Instant CSV drag-and-drop processing from both central viewport and sidebar uploader."),
        ("Persistent Audit Trail", "Historical Compliance", "Session-persistent ingestion history tracking throughput, latency, and row counts across all files."),
        ("Explainable Record Logs", "Per-Row Threat Trigger", "Plain-English explanation detailing the exact threshold or TCP flag that triggered the alert."),
        ("Mitigation Playbooks", "Automated Playbooks", "Prescriptive remediation guidance (e.g. 'Activate TCP SYN cookies, rate-limit source subnet').")
    ]

    for i, (title, tag, desc) in enumerate(dashboard_cards):
        row = i // 3
        col = i % 3
        cx = Inches(0.8 + col * 3.95)
        cy = Inches(1.5 + row * 2.5)
        add_card(s9, cx, cy, Inches(3.8), Inches(2.2))
        
        tb = s9.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.15), Inches(3.4), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = tag.upper()
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = C_BLUE
        
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.space_before = Pt(2)
        
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = C_SLATE
        p.space_before = Pt(6)

    # Example Live Alert Banner
    add_card(s9, Inches(0.8), Inches(6.5), Inches(11.733), Inches(0.7), bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    tb = s9.shapes.add_textbox(Inches(1.0), Inches(6.55), Inches(11.3), Inches(0.6))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "LIVE ALERT DEMO:  [CRITICAL: DoS (SYN Flood)]  |  Trigger: High half-open error rate on service http (100% S0 flag)  |  Action: Activate SYN cookies, drop packets at perimeter"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = C_RED

    s9.notes_slide.notes_text_frame.text = (
        "Our user interface is designed for real-time operations. It includes threat severity donuts, "
        "attack vector bars, and comprehensive logs where every flagged row tells the analyst both WHY "
        "it was flagged and WHAT specific firewall or ACL action to take."
    )

    # =========================================================================
    # SLIDE 10: CONCLUSION & FUTURE PRIORITIES
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10, C_NAVY)

    # Header
    tb = s10.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.733), Inches(1.2))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "CONCLUSION & NEXT PRIORITIES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p = tf.add_paragraph()
    p.text = "Netshield: A Production-Grade Cyber Telemetry Prototype"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.space_before = Pt(4)

    # 4 Pillar Cards
    pillars = [
        ("01", "Delivered Working Prototype", "Fully functional dual-stage engine running locally and on the web with interactive file drag-and-drop and real-time visualization."),
        ("02", "Explainable Threat Profiling", "Eliminates the black-box dilemma by inferring plain-English attack types, severity ratings, and concrete mitigation actions."),
        ("03", "Extreme Line-Rate Speed", "Processes 263,800+ records per second with 3.79 ms latency per 1K batch, perfectly suited for perimeter edge firewalls."),
        ("04", "Clear Engineering Roadmap", "Established architecture ready for online active learning, live eBPF/PCAP network packet sniffing, and SIEM integration.")
    ]
    for i, (num, title, desc) in enumerate(pillars):
        cx = Inches(0.8 + i * 2.95)
        add_card(s10, cx, Inches(2.2), Inches(2.8), Inches(3.2), bg_color=RGBColor(30, 41, 59), border_color=RGBColor(51, 65, 85))
        tb = s10.shapes.add_textbox(cx + Inches(0.15), Inches(2.35), Inches(2.5), Inches(2.9))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = C_CYAN
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p.space_before = Pt(4)
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(6)

    # Next Steps horizontal card
    add_card(s10, Inches(0.8), Inches(5.7), Inches(11.733), Inches(1.3), bg_color=RGBColor(24, 33, 47), border_color=RGBColor(51, 65, 85))
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(5.8), Inches(11.3), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "NEXT ENGINEERING PRIORITIES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p = tf.add_paragraph()
    p.text = "1. Live eBPF / Scapy Sniffer Socket Integration  •  2. Online Incremental Learning with Analyst Feedback  •  3. Automated Webhook Alerts for Splunk & Wazuh SIEM"
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_before = Pt(4)

    s10.notes_slide.notes_text_frame.text = (
        "In summary, Netshield moves cybersecurity anomaly detection from passive academic classification to "
        "active, explainable incident response. We thank the evaluation panel and welcome your questions."
    )

    prs.save(output_path)
    print(f"Presentation generated successfully: {output_path}")

if __name__ == "__main__":
    build_presentation()
