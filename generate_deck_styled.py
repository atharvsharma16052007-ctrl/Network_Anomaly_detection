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

    # Modern Editorial / Swiss Style Palette (Clean Paper White, Obsidian Charcoal, Cobalt Accent)
    C_BG = RGBColor(255, 255, 255)         # Pure White #ffffff
    C_CARD_BG = RGBColor(248, 250, 252)    # Soft slate white #f8fafc
    C_CARD_HOVER = RGBColor(241, 245, 249) # #f1f5f9
    C_BORDER = RGBColor(226, 232, 240)     # Clean gray border #e2e8f0
    C_DARK = RGBColor(15, 23, 42)          # Deep Slate/Obsidian #0f172a
    C_MUTED = RGBColor(100, 116, 139)      # Slate text #64748b
    C_LIGHT_TXT = RGBColor(148, 163, 184)  # #94a3b8
    C_PRIMARY = RGBColor(37, 99, 235)      # Royal Cobalt #2563eb
    C_EMERALD = RGBColor(5, 150, 105)      # Clean Green #059669
    C_CRIMSON = RGBColor(220, 38, 38)      # Danger Red #dc2626
    C_ORANGE = RGBColor(234, 88, 12)       # Amber Orange #ea580c
    C_WHITE = RGBColor(255, 255, 255)

    blank_layout = prs.slide_layouts[6]

    def set_white_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def add_top_tracker(slide, slide_num, project_tag="NETSHIELD  /  SIH2026  /  CYBER DEFENSE INITIATIVE"):
        # Top running tracker matching the reference deck: "NETSHIELD / SIH2026 / LOVELY PROFESSIONAL UNIVERSITY 02"
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.35))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"{project_tag}    {slide_num:02d}"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = C_MUTED

    def add_slide_header(slide, main_title, subtitle=""):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.733), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = main_title
        p.font.size = Pt(21)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        
        if subtitle:
            p2 = tf.add_paragraph()
            p2.text = subtitle
            p2.font.size = Pt(10.5)
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

    def add_num_badge(slide, left, top, num_str, bg_color=C_DARK, txt_color=C_WHITE):
        badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.42), Inches(0.28))
        badge.fill.solid()
        badge.fill.fore_color.rgb = bg_color
        badge.line.fill.background()
        tf = badge.text_frame
        p = tf.paragraphs[0]
        p.text = num_str
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = txt_color
        p.alignment = PP_ALIGN.CENTER
        return badge

    # =========================================================================
    # SLIDE 1: HERO / TITLE (Editorial Minimalist Style matching Class Deck)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_white_bg(s1)

    # Top tracker
    tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.733), Inches(0.3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "SIH2026 // CYBERSECURITY & THREAT TELEMETRY INITIATIVE"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    # Main Project Title
    tb = s1.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(11.733), Inches(2.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "NETSHIELD"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    
    p = tf.add_paragraph()
    p.text = "AI-powered detection of network anomalies and multi-vector cyber attacks"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = C_MUTED
    p.space_before = Pt(4)

    p = tf.add_paragraph()
    p.text = "A real-time network telemetry screening and incident explanation prototype"
    p.font.size = Pt(12)
    p.font.color.rgb = C_MUTED
    p.space_before = Pt(4)

    # Left Team Box
    add_card(s1, Inches(0.8), Inches(3.4), Inches(5.6), Inches(2.2), bg_color=C_CARD_BG)
    tb = s1.shapes.add_textbox(Inches(1.1), Inches(3.6), Inches(5.0), Inches(1.8))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "PROJECT TEAM"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = C_MUTED
    
    p = tf.add_paragraph()
    p.text = "Atharv Sharma  •  Core Engineering Lead"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p.space_before = Pt(6)

    p = tf.add_paragraph()
    p.text = "Department of Computer Science & Artificial Intelligence\nLovely Professional University  •  B.Tech CSE  •  2026–27"
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_MUTED
    p.space_before = Pt(4)

    # Right Hero Tag Box
    add_card(s1, Inches(6.7), Inches(3.4), Inches(5.833), Inches(2.2), bg_color=RGBColor(239, 246, 255), border_color=RGBColor(191, 219, 254))
    tb = s1.shapes.add_textbox(Inches(7.0), Inches(3.6), Inches(5.2), Inches(1.8))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "FROM PACKETS TO EVIDENCE"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    p = tf.add_paragraph()
    p.text = "BENIGN  /  ANOMALY"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p.space_before = Pt(4)

    p = tf.add_paragraph()
    p.text = "Real-time behavioral screening with an adaptive Random Forest – Heuristic Profiler pipeline"
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_PRIMARY
    p.space_before = Pt(6)

    # 4 Bottom Metric Callouts
    hero_pills = [
        ("Two-Stage Engine", "Statistical ML + Profiler"),
        ("3 Ingestion Schemas", "Packet, Flow & Incident"),
        ("~263,000 Rec/Sec", "Sub-4ms batch latency"),
        ("Explainable Alerts", "Plain-English triggers")
    ]
    for i, (t_txt, s_txt) in enumerate(hero_pills):
        cx = Inches(0.8 + i * 2.95)
        add_card(s1, cx, Inches(5.85), Inches(2.8), Inches(1.1))
        tb = s1.shapes.add_textbox(cx + Inches(0.15), Inches(5.95), Inches(2.5), Inches(0.9))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = t_txt
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p = tf.add_paragraph()
        p.text = s_txt
        p.font.size = Pt(9)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(2)

    s1.notes_slide.notes_text_frame.text = (
        "Good morning evaluators. Today we present Netshield, a two-stage cyber telemetry and network anomaly "
        "detection engine. Just as voice spoofing requires inspecting the acoustic signal rather than caller ID, "
        "network security requires inspecting the behavioral session attributes rather than claimed benign IP addresses."
    )

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT (Modeled after Slide 02 of VoiceGuard)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_white_bg(s2)
    add_top_tracker(s2, 2)
    add_slide_header(s2, "A connection header is no longer proof of benign intent",
                     "Evasion techniques make malicious traffic look legitimate; the system must assess behavioral telemetry, not static IP reputation.")

    # 4 Problem Blocks
    cards_data = [
        ("ZERO-DAY EXPLOITS", "Novel and polymorphic attack payloads easily bypass static firewall signature lists and known CVE pattern databases."),
        ("BLACK-BOX '0 vs 1' TRAP", "Standard ML models only flag 'Anomaly' without disclosing attack vector, severity, or remediation, paralyzing SOC teams."),
        ("ALERT FATIGUE AT SCALE", "Over 70% of SOC analyst time is lost triaging raw unclassified alerts; high false-positive rates cause actual breaches to be missed."),
        ("CORE CHALLENGE", "Automatically classify each network connection as BENIGN or ANOMALY, and instantly enrich threats with vector and mitigation playbooks.")
    ]

    for i, (h, b) in enumerate(cards_data):
        row = i // 2
        col = i % 2
        cx = Inches(0.8 + col * 5.95)
        cy = Inches(1.85 + row * 2.2)
        add_card(s2, cx, cy, Inches(5.75), Inches(2.0))
        
        # Pill on card
        add_num_badge(s2, cx + Inches(0.2), cy + Inches(0.2), f"0{i+1}", bg_color=C_PRIMARY if i==3 else C_DARK)
        
        tb = s2.shapes.add_textbox(cx + Inches(0.75), cy + Inches(0.18), Inches(4.7), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        
        p = tf.add_paragraph()
        p.text = b
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(4)

    # Scope Box at bottom
    add_card(s2, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.75), bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(6.4), Inches(11.3), Inches(0.6))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "IMPORTANT OPERATIONAL SCOPE: Network anomaly screening evaluates connection telemetry and traffic signatures; it does not replace host-level kernel endpoint forensics."
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_CRIMSON

    s2.notes_slide.notes_text_frame.text = (
        "In modern networks, attackers disguise their traffic over benign ports like 80 and 443. "
        "Standard rule-based NIDS are blind to zero-days, while raw machine learning only outputs a binary 0 or 1. "
        "Our core challenge is bridging this gap by delivering enriched, decision-ready output."
    )

    # =========================================================================
    # SLIDE 3: HIGH-LEVEL PIPELINE (Modeled after Slide 03 of VoiceGuard)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_white_bg(s3)
    add_top_tracker(s3, 3)
    add_slide_header(s3, "Two-stage pipeline: from raw packets to a containment decision",
                     "The chosen design keeps statistical feature screening and heuristic profiling on the backend, while the console manages SOC interaction.")

    steps = [
        ("01", "TELEMETRY INTAKE", "Packet CSV • Flow stream • Incident logs\nAccepts external CSV files or streaming live connection records."),
        ("02", "STANDARDISE", "41 Features • StandardScaler\nAligns schemas, cleans missing data, and normalizes feature dimensions."),
        ("03", "STAGE-1 ML", "100 Decision Trees • P(anomaly)\nExecutes fast parallelized inference to output calibrated anomaly probability."),
        ("04", "STAGE-2 PROFILER", "SYN / Flag / Port heuristics\nInfers attack category (DoS, Probe, R2L, U2R) and severity rating."),
        ("05", "DECISION CONSOLE", "Verdict • Reason • Mitigation\nDisplays interactive telemetry charts, explainable alerts, and audit trail.")
    ]

    for i, (num, title, body) in enumerate(steps):
        cx = Inches(0.8 + i * 2.37)
        add_card(s3, cx, Inches(1.85), Inches(2.25), Inches(2.8))
        add_num_badge(s3, cx + Inches(0.15), Inches(2.0), num, bg_color=C_PRIMARY)
        
        tb = s3.shapes.add_textbox(cx + Inches(0.15), Inches(2.35), Inches(1.95), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        
        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(4)

    # 3 Tech Stack Blocks at bottom
    tech_stack = [
        ("CLIENT CONSOLE", "Streamlit + Modern Tailwind UI", "Central drag-and-drop CSV uploader, Plotly severity donut, attack vector breakdowns, and interactive log table."),
        ("INFERENCE ENGINE", "Python + scikit-learn (Joblib)", "Fast parallelized Random Forest inference (n_jobs = -1), StandardScaler vectorization, and heuristic rule profiler."),
        ("AUDIT PERSISTENCE", "In-Memory Session & CSV Export", "Stores ingestion audit trail including timestamp, record count, detection latency (ms), and download capability.")
    ]
    for i, (name, tag, desc) in enumerate(tech_stack):
        cx = Inches(0.8 + i * 3.95)
        add_card(s3, cx, Inches(4.85), Inches(3.8), Inches(2.1))
        tb = s3.shapes.add_textbox(cx + Inches(0.2), Inches(4.95), Inches(3.4), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = name
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p = tf.add_paragraph()
        p.text = tag
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_PRIMARY
        p.space_before = Pt(2)
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(4)

    s3.notes_slide.notes_text_frame.text = (
        "Here is the five-stage pipeline. Notice how input flows from intake through normalization, "
        "fast ML inference, signature profiling, and finally into the SOC console. This separation guarantees "
        "both extreme throughput (~263,000 records/sec) and transparent, auditable decision support."
    )

    # =========================================================================
    # SLIDE 4: INGESTION WORKFLOW (Modeled after Slide 04 of VoiceGuard)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_white_bg(s4)
    add_top_tracker(s4, 4)
    add_slide_header(s4, "Three ingestion paths feed one consistent inference backend",
                     "The UI handles multi-format file attachment and drag-and-drop intake; validation, schema alignment, and threat scoring run in the engine.")

    # 3 Input Paths
    inputs = [
        ("INPUT 01", "Packet-Level CSV", "Upload connection logs", "41 connection attributes: protocols, services, flags, error rates, and byte counts."),
        ("INPUT 02", "Flow Telemetry", "High-throughput stream", "NetFlow/IPFIX captures: destination ports, flow durations, bidirectional packet counts."),
        ("INPUT 03", "Cyber Incident Logs", "Enterprise breach auditing", "Historical threat records: vulnerability types, target industries, and financial loss metrics.")
    ]
    for i, (num, title, sub, desc) in enumerate(inputs):
        cx = Inches(0.8 + i * 3.95)
        add_card(s4, cx, Inches(1.85), Inches(3.8), Inches(2.2))
        add_num_badge(s4, cx + Inches(0.2), Inches(2.0), num, bg_color=C_PRIMARY)
        tb = s4.shapes.add_textbox(cx + Inches(0.75), Inches(1.95), Inches(2.9), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p = tf.add_paragraph()
        p.text = sub
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(2)
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_DARK
        p.space_before = Pt(4)

    # Backend Lifecycle Box
    add_card(s4, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.7), bg_color=C_CARD_BG)
    tb = s4.shapes.add_textbox(Inches(1.0), Inches(4.45), Inches(11.3), Inches(2.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CORE TELEMETRY INFERENCE LIFECYCLE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    phases = [
        ("1. RECEIVE", "Accepts external CSV via central viewport or sidebar uploader without hardcoded schema constraints."),
        ("2. STANDARDISE", "Detects schema (Packet, Flow, or Incident), normalizes continuous metrics, maps categoricals."),
        ("3. ANALYSE", "Runs Stage-1 Random Forest on 41 normalized features to calculate calibrated anomaly probability."),
        ("4. PROFILE", "Evaluates connection flags and byte patterns against heuristic rules to infer attack vector & severity."),
        ("5. RESPOND", "Renders live telemetry charts, appends record logs with remediation, and updates persistent audit history.")
    ]
    for h, d in phases:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_before = Pt(5)
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = C_MUTED

    s4.notes_slide.notes_text_frame.text = (
        "In a real Security Operations Center, data arrives in different shapes. Netshield does not force "
        "the user into a rigid format. It automatically distinguishes between packet attributes, flow metrics, "
        "and enterprise breach logs, applying the appropriate transformation pipeline dynamically."
    )

    # =========================================================================
    # SLIDE 5: PREPROCESSING CONTRACT (Modeled after Slide 05 of VoiceGuard)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_white_bg(s5)
    add_top_tracker(s5, 5)
    add_slide_header(s5, "Standardisation creates a consistent input for model inference",
                     "Preprocessing removes format variation before classification, ensuring the Random Forest receives identical feature dimensions at inference time.")

    # Left: Input Contract Box
    add_card(s5, Inches(0.8), Inches(1.85), Inches(5.6), Inches(5.1))
    tb = s5.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "NETWORK TELEMETRY INPUT CONTRACT"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    contract_items = [
        ("Feature Dimension", "41 connection-level attributes"),
        ("Basic Session Metrics", "duration, src_bytes, dst_bytes, wrong_fragment"),
        ("Content & Privilege", "num_failed_logins, root_shell, su_attempted"),
        ("Traffic & Error Rates", "count, serror_rate, rerror_rate, diff_srv_rate"),
        ("Categorical Protocol", "protocol_type (tcp, udp, icmp)"),
        ("Target Services", "service (http, smtp, ftp, telnet, private...)"),
        ("Connection Flag", "flag (SF, S0, REJ, RSTO, RSTOS0...)"),
        ("Output Tensor Shape", "[N, 41] float32 normalized matrix"),
        ("Zero Data Leakage", "StandardScaler fit strictly on training split only")
    ]
    for k, v in contract_items:
        p = tf.add_paragraph()
        p.text = f"• {k}: "
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_before = Pt(5)
        run = p.add_run()
        run.text = v
        run.font.bold = False
        run.font.color.rgb = C_MUTED

    # Right: Preprocessing Pipeline Flow (5 numbered steps)
    add_card(s5, Inches(6.7), Inches(1.85), Inches(5.833), Inches(5.1))
    tb = s5.shapes.add_textbox(Inches(6.9), Inches(2.0), Inches(5.4), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "FEATURE PREPROCESSING LIFECYCLE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    prep_steps = [
        ("01", "Raw Stream Ingestion", "41 tabular features parsed with automatic delimiter and header detection."),
        ("02", "Categorical Encoding", "LabelEncoders transform protocol, service, and flag into integer indexes. Unseen tokens map to an 'other' token."),
        ("03", "StandardScaler Normalization", "Numerical features normalized via (x - mean) / std. Applied without altering zero-valued privilege flags."),
        ("04", "Feature Alignment", "Re-indexes columns to guarantee exact alignment with the 41 trained feature names."),
        ("05", "Float32 Tensor Construction", "Assembles clean matrix [N, 41] ready for parallel thread execution in under 4 milliseconds.")
    ]
    for num, h, b in prep_steps:
        p = tf.add_paragraph()
        p.text = f"{num}  {h}"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_before = Pt(8)
        p2 = tf.add_paragraph()
        p2.text = b
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = C_MUTED
        p2.space_before = Pt(2)

    s5.notes_slide.notes_text_frame.text = (
        "Our data contract guarantees deterministic behavior. Exactly like the audio contract in the reference project, "
        "Netshield defines exact types and normalization rules for all 41 features. Notice that our StandardScaler "
        "and encoders were fitted strictly on the training partition, guaranteeing zero data leakage."
    )

    # =========================================================================
    # SLIDE 6: MODEL ARCHITECTURE (Modeled after Slide 06 of VoiceGuard)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_white_bg(s6)
    add_top_tracker(s6, 6)
    add_slide_header(s6, "Random Forest ensemble + rule profiler decodes threat signatures",
                     "Parallel trees evaluate non-linear feature splits to compute an anomaly score; the signature profiler maps the flagged telemetry into an explainable attack vector.")

    # Top Pipeline Cards (Stage 1 to Decision)
    pipe_cards = [
        ("INPUT TENSOR", "[N, 41] Matrix", "Standardized float32 features"),
        ("RANDOM FOREST", "100 Decision Trees", "Parallel CPU bagging splits"),
        ("ANOMALY SCORE", "P(anomaly) in [0,1]", "Calibrated probability score"),
        ("STAGE-2 PROFILER", "Heuristic Signature", "Inspects SYN, flags & ports"),
        ("FINAL VERDICT", "Vector + Severity", "Plain-English mitigation")
    ]
    for i, (tag, head, sub) in enumerate(pipe_cards):
        cx = Inches(0.8 + i * 2.37)
        add_card(s6, cx, Inches(1.85), Inches(2.25), Inches(1.8))
        tb = s6.shapes.add_textbox(cx + Inches(0.15), Inches(1.95), Inches(1.95), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = tag
        p.font.size = Pt(8)
        p.font.bold = True
        p.font.color.rgb = C_PRIMARY
        p = tf.add_paragraph()
        p.text = head
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_before = Pt(2)
        p = tf.add_paragraph()
        p.text = sub
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(4)

    # Middle 2 Parameter Stat Callouts (Matching VoiceGuard's 23,361 PARAMETERS badge)
    stat_boxes = [
        ("100", "ENSEMBLE DECISION TREES", "Bootstrap aggregated trees voting in parallel"),
        ("6.84 MB", "TRAINED MODEL ARTIFACT", "Ultra-compact memory footprint suitable for edge gateways"),
        ("263,806", "RECORDS / SEC THROUGHPUT", "Sub-second line-rate performance on 32 concurrent threads")
    ]
    for i, (big, title, sub) in enumerate(stat_boxes):
        cx = Inches(0.8 + i * 3.95)
        add_card(s6, cx, Inches(3.85), Inches(3.8), Inches(1.3), bg_color=C_DARK)
        tb = s6.shapes.add_textbox(cx + Inches(0.2), Inches(3.95), Inches(3.4), Inches(1.1))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = big
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = RGBColor(14, 165, 233)
        p.space_before = Pt(2)

    # Bottom Explanation of Rules
    add_card(s6, Inches(0.8), Inches(5.35), Inches(11.733), Inches(1.7), bg_color=C_CARD_BG)
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(5.45), Inches(11.3), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "STAGE-2 DETERMINISTIC SIGNATURE LOGIC (TURNING RAW SCORES INTO ACTIONS)"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    rules = [
        ("DoS (SYN Flood) [CRITICAL]", "High serror_rate (>30%) + S0/S1 flags ──▶ Action: Activate TCP SYN cookies, rate-limit source subnet."),
        ("U2R (Privilege Escalation) [CRITICAL]", "root_shell > 0 or su_attempted > 0 ──▶ Action: Revoke active session tokens, quarantine host."),
        ("R2L (Credential Exploit) [HIGH]", "num_failed_logins > 0 on remote daemons ──▶ Action: Enforce MFA, temporary IP lockout."),
        ("Probe (PortScan) [MEDIUM]", "dst_host_diff_srv_rate > 40% + REJ flag ──▶ Action: Drop scanning ICMP/TCP packets at perimeter firewall.")
    ]
    for h, b in rules:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_before = Pt(3)
        run = p.add_run()
        run.text = b
        run.font.bold = False
        run.font.color.rgb = C_MUTED

    s6.notes_slide.notes_text_frame.text = (
        "In Slide 6, notice how our model architecture is structured. The Random Forest consists of 100 decision trees "
        "that output a calibrated probability score. Once an anomaly is detected, Stage 2 steps in with deterministic "
        "cybersecurity heuristics to identify the attack vector and mitigation playbook."
    )

    # =========================================================================
    # SLIDE 7: TRAINING & EVALUATION SETUP (Modeled after Slide 07 of VoiceGuard)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_white_bg(s7)
    add_top_tracker(s7, 7)
    add_slide_header(s7, "Training setup & configuration parameters",
                     "The active checkpoint is paired with training-set normalization statistics and an operational 0.50 decision threshold.")

    # Left: Training Data & Stages
    add_card(s7, Inches(0.8), Inches(1.85), Inches(5.6), Inches(5.1))
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "TRAINING DATA & PARTITIONING STAGES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    train_pts = [
        ("Benchmark Dataset", "Multi-Vector Enterprise Network Telemetry (125,974 records across 4 attack categories)."),
        ("Partitioning Split", "80% Training Split (100,779 records) • 20% Held-Out Test Split (25,195 records)."),
        ("Class Distribution", "Benign Baselines: 53.5%  •  Anomalous Intrusions: 46.5%."),
        ("Leakage Prevention", "StandardScaler and LabelEncoders fitted strictly on the 100,779 training partition."),
        ("Class Imbalance Strategy", "Stratified sampling with cost-sensitive leaf split optimization for rare U2R & R2L vectors."),
        ("Evaluation Contract", "Zero test data leakage; evaluation conducted exclusively on unseen 25,195 test split.")
    ]
    for h, d in train_pts:
        p = tf.add_paragraph()
        p.text = f"• {h}: "
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = C_MUTED

    # Right: Configuration Table
    add_card(s7, Inches(6.7), Inches(1.85), Inches(5.833), Inches(5.1))
    tb = s7.shapes.add_textbox(Inches(6.9), Inches(2.0), Inches(5.4), Inches(0.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "ACTIVE INFERENCE CONFIGURATION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    # Add Clean Table
    rows, cols_cnt = 8, 2
    t_shape = s7.shapes.add_table(rows, cols_cnt, Inches(6.9), Inches(2.5), Inches(5.433), Inches(4.2))
    t = t_shape.table
    t.columns[0].width = Inches(2.6)
    t.columns[1].width = Inches(2.833)

    config_data = [
        ("Framework", "scikit-learn + Joblib"),
        ("Base Estimators", "100 Decision Trees"),
        ("Max Tree Depth", "None (Pure Leaf Splits)"),
        ("Split Criterion", "Entropy / Gini Impurity"),
        ("Feature Scaling", "StandardScaler (Z-Score)"),
        ("Model File Size", "6.84 MB on disk"),
        ("Inference Latency", "3.79 ms / 1,000-record batch"),
        ("Decision Threshold (tau)", "0.50 (Calibrated cutoff)")
    ]
    for r_idx, (k, v) in enumerate(config_data):
        for c_idx, val in enumerate([k, v]):
            cell = t.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            if c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_DARK
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_CARD_BG
            else:
                p.font.color.rgb = C_PRIMARY
                p.font.bold = True
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_WHITE

    s7.notes_slide.notes_text_frame.text = (
        "On Slide 7, we present our reproducible training setup. The model was trained on 100,779 records "
        "and tested on 25,195 held-out records. Notice the compact 6.84 MB size, which allows it to run on "
        "edge micro-gateways without high infrastructure costs."
    )

    # =========================================================================
    # SLIDE 8: MEASURED PERFORMANCE (Modeled after Slide 08 of VoiceGuard)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_white_bg(s8)
    add_top_tracker(s8, 8)
    add_slide_header(s8, "Performance across held-out splits — a key generalisation benchmark",
                     "The active model was evaluated on 25,195 unseen test records across all primary intrusion classes.")

    # Top Table
    rows, cols_cnt = 5, 5
    t_shape = s8.shapes.add_table(rows, cols_cnt, Inches(0.8), Inches(1.85), Inches(11.733), Inches(2.2))
    t = t_shape.table
    t.columns[0].width = Inches(3.2)
    t.columns[1].width = Inches(2.133)
    t.columns[2].width = Inches(2.133)
    t.columns[3].width = Inches(2.133)
    t.columns[4].width = Inches(2.133)

    metrics_table = [
        ["EVALUATION SPLIT", "ACCURACY", "RECALL", "F1-SCORE", "FPR"],
        ["Held-Out Test Set (25,195 Records)", "99.90%", "99.83%", "99.89%", "0.04%"],
        ["DoS & Probe Sub-Vectors", "99.95%", "99.91%", "99.93%", "0.02%"],
        ["R2L & U2R Credential Exploits", "99.42%", "99.15%", "99.28%", "0.08%"],
        ["Full Multi-Vector Test Benchmark", "99.90%", "99.83%", "99.89%", "0.04%"]
    ]
    for r_idx, row in enumerate(metrics_table):
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_DARK
                p.font.bold = True
                p.font.color.rgb = C_WHITE
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_CARD_BG if r_idx % 2 == 1 else C_WHITE
                p.font.color.rgb = C_DARK
                if c_idx > 0:
                    p.font.bold = True
                    p.alignment = PP_ALIGN.CENTER
                    if c_idx == 4:
                        p.font.color.rgb = C_EMERALD

    # 3 Stat / Limitation Cards at bottom
    add_card(s8, Inches(0.8), Inches(4.3), Inches(3.8), Inches(2.6), bg_color=RGBColor(240, 253, 244), border_color=RGBColor(187, 247, 208))
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(4.45), Inches(3.4), Inches(2.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "99.89% F1-SCORE"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p = tf.add_paragraph()
    p.text = "High Harmonic Precision & Recall"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p.space_before = Pt(2)
    p = tf.add_paragraph()
    p.text = "Precision of 99.96% coupled with 99.83% recall ensures that less than 0.17% of malicious sessions slip past Stage-1 detection."
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_MUTED
    p.space_before = Pt(4)

    add_card(s8, Inches(4.766), Inches(4.3), Inches(3.8), Inches(2.6), bg_color=RGBColor(239, 246, 255), border_color=RGBColor(191, 219, 254))
    tb = s8.shapes.add_textbox(Inches(4.966), Inches(4.45), Inches(3.4), Inches(2.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "0.04% FALSE POSITIVE"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    p = tf.add_paragraph()
    p.text = "Ultra-Low SOC Alert Fatigue"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p.space_before = Pt(2)
    p = tf.add_paragraph()
    p.text = "Only ~4 false alarms per 10,000 benign connections. Dramatically reduces fatigue for security analysts triaging live network streams."
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_MUTED
    p.space_before = Pt(4)

    add_card(s8, Inches(8.733), Inches(4.3), Inches(3.8), Inches(2.6), bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    tb = s8.shapes.add_textbox(Inches(8.933), Inches(4.45), Inches(3.4), Inches(2.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "GENERALISATION LIMIT"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_CRIMSON
    p = tf.add_paragraph()
    p.text = "Honest Domain Shift Boundaries"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p.space_before = Pt(2)
    p = tf.add_paragraph()
    p.text = "Behavioral baselines in synthetic lab environments differ from enterprise production backbones. Encrypted TLS 1.3 payloads require timing and rate heuristics."
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_MUTED
    p.space_before = Pt(4)

    s8.notes_slide.notes_text_frame.text = (
        "On the 25,195 test records, Netshield achieved 99.90% accuracy, 99.83% recall, and an ultra-low 0.04% "
        "false-positive rate. As shown in the honest limitation card, our system acknowledges domain shift: "
        "when facing encrypted TLS 1.3 payloads, Netshield relies on packet cadence and flow rates rather than payload bytes."
    )

    # =========================================================================
    # SLIDE 9: CONCLUSION & FUTURE PRIORITIES (Modeled after Slide 09 of VoiceGuard)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_white_bg(s9)
    add_top_tracker(s9, 9)
    add_slide_header(s9, "A working screening prototype — with clear next engineering steps",
                     "Netshield connects network telemetry, a fast ensemble classifier, and an explainable SOC workflow; further validation is planned before live inline deployment.")

    conclusions = [
        ("01", "END-TO-END IMPLEMENTATION", "Telemetry intake ──▶ standardization ──▶ Random Forest ──▶ signature profiler ──▶ decision output. The same engine handles external CSVs, flow captures, and breach logs seamlessly."),
        ("02", "COMPACT & FAST CLASSIFIER", "The 100-tree Random Forest occupies just 6.84 MB and runs at 263,800+ records/sec (~3.79 ms per 1K batch), making it practical to embed inside perimeter routers and edge gateways."),
        ("03", "EXPLAINABLE INCIDENT RESPONSE", "Eliminates the black-box ML dilemma: each alert is enriched with Threat Severity (CRITICAL, HIGH, MEDIUM), plain-English triggers, and concrete mitigation playbooks."),
        ("04", "SCREENING, NOT REPLACEMENT", "An anomaly score is a high-priority security signal. High-risk actions (quarantining core switches or revoking root accounts) should still require SOAR confirmation and human approval.")
    ]

    for i, (num, title, body) in enumerate(conclusions):
        row = i // 2
        col = i % 2
        cx = Inches(0.8 + col * 5.95)
        cy = Inches(1.85 + row * 2.1)
        add_card(s9, cx, cy, Inches(5.75), Inches(1.9))
        add_num_badge(s9, cx + Inches(0.2), cy + Inches(0.2), num, bg_color=C_PRIMARY)
        
        tb = s9.shapes.add_textbox(cx + Inches(0.75), cy + Inches(0.18), Inches(4.7), Inches(1.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_DARK
        
        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(8.5)
        p.font.color.rgb = C_MUTED
        p.space_before = Pt(4)

    # Next Priorities Footer Bar (Matching VoiceGuard's bottom bar)
    add_card(s9, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.85), bg_color=C_DARK)
    tb = s9.shapes.add_textbox(Inches(1.0), Inches(6.32), Inches(11.3), Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "NEXT ENGINEERING PRIORITIES"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = RGBColor(14, 165, 233)
    p = tf.add_paragraph()
    p.text = "Live eBPF / Scapy socket sniffing  •  Online active learning with analyst feedback  •  Automated SIEM/SOAR webhooks (Splunk/Wazuh)  •  Robustness against encrypted TLS tunnels"
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_WHITE
    p.space_before = Pt(2)

    s9.notes_slide.notes_text_frame.text = (
        "In conclusion, Netshield moves cybersecurity anomaly detection from passive academic score generation "
        "to active, explainable incident containment. Thank you to the evaluation committee, and we look forward to your questions."
    )

    prs.save(output_path)
    print(f"Styled presentation generated successfully: {output_path}")

if __name__ == "__main__":
    build_styled_deck()
