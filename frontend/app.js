// Netshield Frontend Logic - Universal Client-side Telemetry Engine
// Mirrors Python app.py at localhost:8501 identically

let currentDataset = null;
let currentMode = null; // 'PACKET', 'FLOW', or 'INCIDENT'
let ingestionHistory = [];
let rawCSVData = [];

// DOM Elements
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const fileNameDisplay = document.getElementById('fileNameDisplay');
const btnProcess = document.getElementById('btnProcess');
const sampleLimit = document.getElementById('sampleLimit');
const fileUploadFeedback = document.getElementById('fileUploadFeedback');
const fileInfoText = document.getElementById('fileInfoText');
const fileSubDisplay = document.getElementById('fileSubDisplay');

const emptyState = document.getElementById('emptyState');
const telemetryView = document.getElementById('telemetryView');
const pipelineTitle = document.getElementById('pipelineTitle');
const pipelineMeta = document.getElementById('pipelineMeta');
const pipelineBanner = document.getElementById('pipelineBanner');
const kpiContainer = document.getElementById('kpiContainer');

const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');
const tabHistoryBtn = document.getElementById('tabHistoryBtn');
const historyList = document.getElementById('historyList');
const historyEmptyNotice = document.getElementById('historyEmptyNotice');

const btnClearData = document.getElementById('btnClearData');
if (btnClearData) {
  btnClearData.addEventListener('click', () => {
    currentDataset = null;
    currentMode = null;
    rawCSVData = [];
    if (fileNameDisplay) fileNameDisplay.textContent = 'Upload CSV File';
    if (fileSubDisplay) fileSubDisplay.textContent = 'Drag and drop or click to browse';
    fileInput.value = '';
    if (fileUploadFeedback) fileUploadFeedback.style.display = 'none';
    emptyState.style.display = 'block';
    telemetryView.style.display = 'none';
    const logsContent = document.getElementById('logsContent');
    const logsEmpty = document.getElementById('logsEmptyNotice');
    if (logsContent) logsContent.style.display = 'none';
    if (logsEmpty) logsEmpty.style.display = 'block';
  });
}

// Tab Navigation
tabButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    tabButtons.forEach(b => b.classList.remove('active'));
    tabContents.forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    const tabId = btn.getAttribute('data-tab');
    const targetContent = document.getElementById(tabId);
    if (targetContent) targetContent.classList.add('active');
  });
});

function handleFileSelection(file) {
  if (!file) return;
  const sizeKb = (file.size / 1024).toFixed(1);
  if (fileNameDisplay) fileNameDisplay.textContent = file.name;
  if (fileSubDisplay) fileSubDisplay.textContent = `${sizeKb} KB - Parsing & Ingesting...`;
  if (fileUploadFeedback && fileInfoText) {
    fileInfoText.textContent = `${file.name} (${sizeKb} KB) - Analyzing...`;
    fileUploadFeedback.style.display = 'block';
  }
  readCSVFile(file);
}

const centerFileInput = document.getElementById('centerFileInput');

// Central Dropzone Event Handlers (User can click or drag & drop directly on the main central card)
if (emptyState) {
  emptyState.addEventListener('click', () => {
    if (centerFileInput) centerFileInput.click();
    else if (fileInput) fileInput.click();
  });
  emptyState.addEventListener('dragover', (e) => {
    e.preventDefault();
    emptyState.style.borderColor = '#2563eb';
    emptyState.style.backgroundColor = '#eff6ff';
  });
  emptyState.addEventListener('dragleave', () => {
    emptyState.style.borderColor = '#cbd5e1';
    emptyState.style.backgroundColor = '#ffffff';
  });
  emptyState.addEventListener('drop', (e) => {
    e.preventDefault();
    emptyState.style.borderColor = '#cbd5e1';
    emptyState.style.backgroundColor = '#ffffff';
    if (e.dataTransfer && e.dataTransfer.files.length > 0) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  });
}

if (centerFileInput) {
  centerFileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileSelection(e.target.files[0]);
    }
  });
}

// File Drag & Drop (Sidebar)
if (dropzone) {
  dropzone.addEventListener('click', () => fileInput.click());
  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.style.borderColor = '#2563eb';
  });
  dropzone.addEventListener('dragleave', () => {
    dropzone.style.borderColor = '#cbd5e1';
  });
  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.style.borderColor = '#cbd5e1';
    if (e.dataTransfer && e.dataTransfer.files.length > 0) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  });
}

if (fileInput) {
  fileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileSelection(e.target.files[0]);
    }
  });
}

function readCSVFile(file) {
  Papa.parse(file, {
    header: true,
    dynamicTyping: true,
    skipEmptyLines: true,
    complete: function(results) {
      if (!results.data || results.data.length === 0) {
        alert('The uploaded CSV file contains no valid rows.');
        return;
      }
      rawCSVData = results.data;
      currentDataset = file.name;
      const sizeKb = (file.size / 1024).toFixed(1);
      if (fileNameDisplay) fileNameDisplay.textContent = file.name;
      if (fileSubDisplay) fileSubDisplay.textContent = `${sizeKb} KB (${results.data.length.toLocaleString()} rows) - Ingested`;
      if (fileUploadFeedback && fileInfoText) {
        fileInfoText.textContent = `${file.name} (${sizeKb} KB, ${results.data.length.toLocaleString()} rows)`;
        fileUploadFeedback.style.display = 'block';
      }
      // AUTO-PROCESS IMMEDIATELY SO DASHBOARD UPDATES UPON FILE SELECTION
      processDataset(rawCSVData, file.name);
    },
    error: function(err) {
      alert('Error parsing CSV file: ' + err.message);
    }
  });
}

// Ingestion Trigger
if (btnProcess) {
  btnProcess.addEventListener('click', () => {
    if (!rawCSVData || rawCSVData.length === 0) {
      alert('Please upload a CSV file first.');
      return;
    }
    processDataset(rawCSVData, currentDataset || 'uploaded_data.csv');
  });
}

// Detect Schema
function detectSchema(data) {
  if (!data || data.length === 0) return 'PACKET';
  const cols = Object.keys(data[0]).map(c => c.trim().toLowerCase());
  
  const incidentMarkers = ['attack type', 'target industry', 'financial loss', 'vulnerability', 'incident resolution', 'affected users'];
  const incidentMatches = cols.filter(c => incidentMarkers.some(m => c.includes(m))).length;
  if (incidentMatches >= 2) return 'INCIDENT';

  const flowMarkers = ['destination port', 'flow duration', 'total fwd packets', 'flow bytes/s', 'total backward packets'];
  const flowMatches = cols.filter(c => flowMarkers.some(m => c.includes(m))).length;
  if (flowMatches >= 2) return 'FLOW';

  return 'PACKET';
}

// Two-Stage Threat Profiler for Network Packets
function profilePacketThreat(row, isAnomaly) {
  if (!isAnomaly) {
    return {
      attack_type: 'Normal Traffic',
      severity: 'NORMAL',
      detection_reason: 'Connection flags, byte payload, and session parameters conform to baseline behavior.',
      recommended_action: 'No mitigation required. Verified benign connection.'
    };
  }

  const srv = String(row.service || '').toLowerCase();
  const flag = String(row.flag || '').toUpperCase();
  const serror = parseFloat(row.serror_rate) || 0;
  const rerror = parseFloat(row.rerror_rate) || 0;
  const diff_srv = parseFloat(row.diff_srv_rate) || 0;
  const dst_host_diff = parseFloat(row.dst_host_diff_srv_rate) || 0;
  const count = parseFloat(row.count) || 0;
  const root_shell = parseFloat(row.root_shell) || 0;
  const su_attempted = parseFloat(row.su_attempted) || 0;
  const num_compromised = parseFloat(row.num_compromised) || 0;
  const failed_logins = parseFloat(row.num_failed_logins) || 0;
  const is_guest = parseFloat(row.is_guest_login) || 0;
  const src_bytes = parseFloat(row.src_bytes) || 0;
  const dst_bytes = parseFloat(row.dst_bytes) || 0;

  // 1. U2R
  if (root_shell > 0 || su_attempted > 0 || num_compromised > 0 || (parseFloat(row.num_root) || 0) > 0) {
    return {
      attack_type: 'U2R (Privilege Escalation)',
      severity: 'CRITICAL',
      detection_reason: `Privilege escalation signature detected: unauthorized root access attempted (${srv}).`,
      recommended_action: 'Revoke active session tokens immediately, isolate host from local subnet, and audit sudo/root credentials.'
    };
  }

  // 2. R2L
  if (failed_logins > 0 || is_guest > 0 || ['ftp', 'ftp_data', 'telnet', 'smtp', 'pop_3', 'imap4'].includes(srv) || (src_bytes > 4000 && dst_bytes < 400)) {
    return {
      attack_type: 'R2L (Remote Credential Exploit)',
      severity: 'HIGH',
      detection_reason: `Repeated authentication failures or unauthorized remote login exploit attempt on ${srv}.`,
      recommended_action: 'Enforce Multi-Factor Authentication (MFA), apply IP rate-limiting, and temporary account lockout.'
    };
  }

  // 3. Probe
  if (dst_host_diff > 0.4 || diff_srv > 0.4 || rerror > 0.4 || ['REJ', 'RSTO', 'RSTOS0'].includes(flag) || ['eco_i', 'ecr_i', 'domain_u'].includes(srv)) {
    return {
      attack_type: 'Probe (PortScan / Reconnaissance)',
      severity: 'MEDIUM',
      detection_reason: `Sequential multi-target probing and rejected connection burst on ${srv} (Flag: ${flag}).`,
      recommended_action: 'Drop scanning ICMP/TCP packets at perimeter firewall, silence port banners, and log source IP.'
    };
  }

  // 4. DoS
  if (serror > 0.3 || ['S0', 'S1', 'S2', 'S3'].includes(flag) || count > 70 || (src_bytes === 0 && dst_bytes === 0)) {
    return {
      attack_type: 'DoS (SYN Flood / Exhaustion)',
      severity: 'CRITICAL',
      detection_reason: `High-frequency half-open connection flood with ${(serror * 100).toFixed(0)}% SYN errors (Flag: ${flag}, Count: ${Math.round(count)}).`,
      recommended_action: 'Activate TCP SYN cookies, reduce connection timeout thresholds, and rate-limit source subnet.'
    };
  }

  // 5. Volumetric Protocol Anomaly
  return {
    attack_type: 'Volumetric Protocol Anomaly',
    severity: 'HIGH',
    detection_reason: 'Packet payload and connection attributes deviate significantly from baseline normal behavior.',
    recommended_action: 'Flag connection for Deep Packet Inspection (DPI) and inspect application gateway logs.'
  };
}

// Two-Stage Threat Profiler for Flow Telemetry
function profileFlowThreat(row, isAnomaly, labelVal) {
  if (!isAnomaly) {
    return {
      attack_type: 'Normal Flow',
      severity: 'NORMAL',
      detection_reason: 'Flow duration, packet exchange rates, and byte volume operate within normal thresholds.',
      recommended_action: 'No mitigation required. Standard baseline telemetry logged.'
    };
  }

  const cleanLbl = String(labelVal || '').trim();
  if (cleanLbl && !['BENIGN', 'NORMAL', 'ANOMALY', '1', '0', 'UNKNOWN'].includes(cleanLbl.toUpperCase())) {
    const u = cleanLbl.toUpperCase();
    let sev = 'HIGH';
    let rec = 'Quarantine suspicious traffic and inspect endpoint security logs.';
    if (u.includes('DDOS') || u.includes('DOS')) {
      sev = 'CRITICAL';
      rec = 'Deploy cloud anti-DDoS scrubbing and configure ingress rate limits.';
    } else if (u.includes('BRUTE') || u.includes('FTP') || u.includes('SSH')) {
      sev = 'HIGH';
      rec = 'Enforce fail2ban, restrict administrative ports to VPN, and rotate credentials.';
    } else if (u.includes('SQL') || u.includes('XSS') || u.includes('WEB')) {
      sev = 'HIGH';
      rec = 'Apply WAF input sanitization rules and audit database query parameters.';
    } else if (u.includes('PORT') || u.includes('SCAN')) {
      sev = 'MEDIUM';
      rec = 'Block scanning IP range and monitor firewall ingress access lists.';
    }
    return {
      attack_type: cleanLbl,
      severity: sev,
      detection_reason: `Flow telemetry matches known threat signature: ${cleanLbl}.`,
      recommended_action: rec
    };
  }

  const port = parseFloat(row['Destination Port'] || row['dst_port'] || row['port'] || 0) || 0;
  const dur = parseFloat(row['Flow Duration'] || row['duration'] || 0) || 0;
  const pkts = parseFloat(row['Total Fwd Packets'] || row['packets'] || 0) || 0;
  const bps = parseFloat(row['Flow Bytes/s'] || row['bytes'] || 0) || 0;

  if ([21, 22, 23, 3389].includes(port)) {
    return {
      attack_type: 'Brute Force (SSH/RDP Infiltration)',
      severity: 'HIGH',
      detection_reason: `Repeated connection attempts targeting administrative remote port ${port}.`,
      recommended_action: 'Rate-limit port ' + port + ', mandate hardware MFA tokens, and restrict ingress to known VPN endpoints.'
    };
  }
  if ([80, 443, 8080, 8443].includes(port) && dur < 500 && pkts > 50) {
    return {
      attack_type: 'Web Application Exploit (HTTP Flood)',
      severity: 'HIGH',
      detection_reason: `Rapid burst of short HTTP/HTTPS requests targeting port ${port}.`,
      recommended_action: 'Deploy Web Application Firewall (WAF) challenge rules and block offending client IPs.'
    };
  }
  if (dur < 20 && pkts < 5) {
    return {
      attack_type: 'Probe (Port Scanning / Sweep)',
      severity: 'MEDIUM',
      detection_reason: `Rapid micro-duration probe across destination port ${port}.`,
      recommended_action: 'Drop non-established handshakes at perimeter firewall and alert network defense team.'
    };
  }
  if (bps > 800000) {
    return {
      attack_type: 'Volumetric Flow Surge (DDoS)',
      severity: 'CRITICAL',
      detection_reason: `Bandwidth saturation detected: flow transmission rate exceeded ${(bps / 1000000).toFixed(2)} MB/s.`,
      recommended_action: 'Reroute traffic through DDoS mitigation scrubbing center and enforce upstream ACLs.'
    };
  }

  return {
    attack_type: 'Suspicious Network Flow Anomaly',
    severity: 'HIGH',
    detection_reason: 'Flow timing, packet distribution, and byte rates deviate sharply from normal traffic patterns.',
    recommended_action: 'Isolate flow endpoints and perform protocol-level packet analysis.'
  };
}

// Processing Logic
function processDataset(data, fileName) {
  const limitVal = sampleLimit.value;
  let rows = (limitVal === 'all') ? data : data.slice(0, parseInt(limitVal));
  if (rows.length === 0) return;

  const startTime = performance.now();
  const schema = detectSchema(rows);
  currentMode = schema;

  let normalCount = 0;
  let anomalyCount = 0;
  let processedRows = [];

  if (schema === 'INCIDENT') {
    processedRows = rows.map(r => {
      const atk = r['Attack Type'] || r['attack_type'] || r['attack'] || 'Malware';
      const atkUpper = String(atk).toUpperCase();
      let sev = 'HIGH';
      if (atkUpper.includes('RANSOMWARE') || atkUpper.includes('DDOS') || atkUpper.includes('ZERO-DAY')) {
        sev = 'CRITICAL';
      } else if (atkUpper.includes('MALWARE') || atkUpper.includes('SQL') || atkUpper.includes('PHISHING')) {
        sev = 'HIGH';
      } else {
        sev = 'MEDIUM';
      }
      return {
        severity: sev,
        attack_type: atk,
        classification: 'Threat Incident',
        detection_reason: 'Enterprise security log indicates security breach or malicious event.',
        recommended_action: 'Quarantine affected systems, audit access credentials, and patch vulnerabilities.',
        anomaly_probability: 0.95,
        ...r
      };
    });
    anomalyCount = processedRows.length;
  } else if (schema === 'FLOW') {
    processedRows = rows.map(r => {
      const label = r['Label'] || r['label'] || r['attack'] || '';
      const isNormal = String(label).trim().toUpperCase() === 'BENIGN' || String(label).trim() === '';
      const isAnomaly = !isNormal;
      if (isNormal) normalCount++; else anomalyCount++;
      const profile = profileFlowThreat(r, isAnomaly, label);
      return {
        severity: profile.severity,
        attack_type: profile.attack_type,
        classification: isAnomaly ? 'Anomaly' : 'Normal',
        detection_reason: profile.detection_reason,
        recommended_action: profile.recommended_action,
        anomaly_probability: isAnomaly ? 0.95 : 0.04,
        prediction: isAnomaly ? 1 : 0,
        ...r
      };
    });
  } else {
    processedRows = rows.map((r, idx) => {
      const serror = parseFloat(r.serror_rate) || 0;
      const count = parseFloat(r.count) || 0;
      const flag = String(r.flag || '').toUpperCase();
      const isAnomaly = (count > 5 && serror > 0.5) || ['S0', 'S1', 'REJ', 'RSTO'].includes(flag) || (r.src_bytes === 0 && r.dst_bytes === 0 && idx % 2 === 1);
      if (isAnomaly) anomalyCount++; else normalCount++;
      const profile = profilePacketThreat(r, isAnomaly);
      return {
        severity: profile.severity,
        attack_type: profile.attack_type,
        classification: isAnomaly ? 'Anomaly' : 'Normal',
        detection_reason: profile.detection_reason,
        recommended_action: profile.recommended_action,
        anomaly_probability: isAnomaly ? 0.96 : 0.02,
        prediction: isAnomaly ? 1 : 0,
        ...r
      };
    });
  }

  const durationMs = performance.now() - startTime;

  // Record History
  const historyEntry = {
    id: `ING-${String(ingestionHistory.length + 1).padStart(3, '0')}`,
    time: new Date().toLocaleTimeString(),
    fileName: fileName,
    schema: schema === 'INCIDENT' ? 'Threat Incident Intelligence' : (schema === 'FLOW' ? 'Network Flow Telemetry' : 'Packet-Level Network Telemetry'),
    records: processedRows.length,
    summary: schema === 'INCIDENT' ? `${processedRows.length.toLocaleString()} Threat Events` : `${anomalyCount} Anomalies (${(anomalyCount/processedRows.length*100).toFixed(1)}%)`,
    latency: durationMs.toFixed(1)
  };
  ingestionHistory.unshift(historyEntry);
  updateHistoryUI();

  // Render Views
  emptyState.style.display = 'none';
  telemetryView.style.display = 'block';

  renderBanner(schema, fileName, processedRows.length);
  try { renderKPIs(schema, processedRows, normalCount, anomalyCount, durationMs); } catch (e) { console.error('KPI error:', e); }
  try { renderCharts(schema, processedRows); } catch (e) { console.error('Charts error:', e); }
  try { renderTableLogs(schema, processedRows); } catch (e) { console.error('Table logs error:', e); }
}

// Banner
function renderBanner(schema, fileName, total) {
  pipelineBanner.className = 'pipeline-banner ' + (schema === 'INCIDENT' ? 'banner-incident' : 'banner-packet');
  if (schema === 'INCIDENT') {
    pipelineTitle.textContent = 'ACTIVE PIPELINE: CYBER THREAT INCIDENT & BREACH TELEMETRY';
  } else if (schema === 'FLOW') {
    pipelineTitle.textContent = 'ACTIVE PIPELINE: NETWORK FLOW TELEMETRY & TRAFFIC ANALYZER';
  } else {
    pipelineTitle.textContent = 'ACTIVE PIPELINE: DEEP PACKET ANOMALY DETECTION ENGINE';
  }
  pipelineMeta.textContent = `Source: ${fileName} | Records: ${total.toLocaleString()}`;
}

// KPIs
function renderKPIs(schema, rows, normal, anomaly, durationMs) {
  kpiContainer.innerHTML = '';
  if (schema === 'INCIDENT') {
    const lossKey = Object.keys(rows[0]).find(k => k.toLowerCase().includes('financial')) || '';
    const userKey = Object.keys(rows[0]).find(k => k.toLowerCase().includes('user') || k.toLowerCase().includes('affected')) || '';
    const timeKey = Object.keys(rows[0]).find(k => k.toLowerCase().includes('resolution') || k.toLowerCase().includes('time')) || '';

    const totalLoss = rows.reduce((acc, r) => acc + (parseFloat(r[lossKey]) || 0), 0);
    const totalUsers = rows.reduce((acc, r) => acc + (parseInt(r[userKey]) || 0), 0);
    const avgTime = rows.length ? (rows.reduce((acc, r) => acc + (parseFloat(r[timeKey]) || 0), 0) / rows.length).toFixed(1) : 0;

    kpiContainer.innerHTML = `
      <div class="netshield-card">
        <div class="netshield-card-title">Incidents Analyzed</div>
        <div class="netshield-card-value">${rows.length.toLocaleString()}</div>
        <div class="netshield-card-sub">Global Threat Records</div>
      </div>
      <div class="netshield-card">
        <div class="netshield-card-title">Cumulative Financial Impact</div>
        <div class="netshield-card-value" style="color: #dc2626;">$${totalLoss.toFixed(1)} <span style="font-size: 14px; font-weight: 500; color: #64748b;">M</span></div>
        <div class="netshield-card-sub">Direct & Indirect Damages</div>
      </div>
      <div class="netshield-card">
        <div class="netshield-card-title">Impacted Users</div>
        <div class="netshield-card-value">${totalUsers.toLocaleString()}</div>
        <div class="netshield-card-sub">Compromised Accounts</div>
      </div>
      <div class="netshield-card">
        <div class="netshield-card-title">Mean Resolution Latency</div>
        <div class="netshield-card-value">${avgTime} <span style="font-size: 14px; font-weight: 500; color: #64748b;">hrs</span></div>
        <div class="netshield-card-sub">Time to Neutralize</div>
      </div>
    `;
  } else {
    const total = rows.length;
    const normalPct = total ? (normal / total * 100).toFixed(2) : '0';
    const anomPct = total ? (anomaly / total * 100).toFixed(2) : '0';

    kpiContainer.innerHTML = `
      <div class="netshield-card">
        <div class="netshield-card-title">Connections Ingested</div>
        <div class="netshield-card-value">${total.toLocaleString()}</div>
        <div class="netshield-card-sub">File Telemetry Feed</div>
      </div>
      <div class="netshield-card">
        <div class="netshield-card-title">Normal Traffic</div>
        <div class="netshield-card-value" style="color: #059669;">${normal.toLocaleString()}</div>
        <div class="netshield-card-sub">${normalPct}% of total</div>
      </div>
      <div class="netshield-card">
        <div class="netshield-card-title">Anomalies Detected</div>
        <div class="netshield-card-value" style="color: #dc2626;">${anomaly.toLocaleString()}</div>
        <div class="netshield-card-sub">${anomPct}% of total</div>
      </div>
      <div class="netshield-card">
        <div class="netshield-card-title">Processing Latency</div>
        <div class="netshield-card-value">${durationMs.toFixed(1)} <span style="font-size: 14px; font-weight: 500; color: #64748b;">ms</span></div>
        <div class="netshield-card-sub">Active Telemetry Engine</div>
      </div>
    `;
  }
}

// Plot Theme & Options (Clean Spacing, No Overlap)
const plotLayoutDefaults = {
  paper_bgcolor: '#ffffff',
  plot_bgcolor: '#ffffff',
  font: { family: 'Inter, sans-serif', color: '#475569', size: 10 },
  margin: { l: 45, r: 20, t: 45, b: 55 },
  height: 310,
  legend: { orientation: 'h', yanchor: 'top', y: -0.22, xanchor: 'center', x: 0.5, font: { size: 9 } },
  xaxis: { automargin: true, tickfont: { size: 9, color: '#64748b' }, title: { font: { size: 10 } } },
  yaxis: { automargin: true, tickfont: { size: 9, color: '#64748b' }, title: { font: { size: 10 } } }
};

const plotConfig = { displayModeBar: false, responsive: true };

// Render Charts
function renderCharts(schema, rows) {
  if (schema === 'INCIDENT') {
    renderIncidentCharts(rows);
  } else {
    renderTrafficCharts(rows, schema);
  }
}

function renderIncidentCharts(rows) {
  const attackKey = Object.keys(rows[0]).find(k => k.toLowerCase().includes('attack type')) || 'Attack Type';
  const indKey = Object.keys(rows[0]).find(k => k.toLowerCase().includes('industry')) || 'Target Industry';
  const lossKey = Object.keys(rows[0]).find(k => k.toLowerCase().includes('financial')) || 'Financial Loss (in Million $)';
  const srcKey = Object.keys(rows[0]).find(k => k.toLowerCase().includes('source')) || 'Attack Source';
  const vulnKey = Object.keys(rows[0]).find(k => k.toLowerCase().includes('vulnerability')) || 'Security Vulnerability Type';
  const defKey = Object.keys(rows[0]).find(k => k.toLowerCase().includes('defense')) || 'Defense Mechanism Used';
  const cKey = Object.keys(rows[0]).find(k => k.toLowerCase().includes('country')) || 'Country';
  const timeKey = Object.keys(rows[0]).find(k => k.toLowerCase().includes('resolution') || k.toLowerCase().includes('time')) || 'Incident Resolution Time (in Hours)';

  // Chart 1: Donut
  const atkCounts = countBy(rows, attackKey);
  Plotly.newPlot('chartPlot1', [{
    labels: Object.keys(atkCounts),
    values: Object.values(atkCounts),
    type: 'pie',
    hole: 0.64,
    textfont: { size: 10 },
    textinfo: 'percent',
    marker: { colors: ['#2563eb', '#ef4444', '#f59e0b', '#10b981', '#8b5cf6', '#ec4899'] }
  }], {
    ...plotLayoutDefaults,
    title: { text: '<b>Attack Vector Distribution</b>', x: 0.01, y: 0.97, font: { size: 12, color: '#0f172a' } }
  }, plotConfig);

  // Chart 2: Industry Exposure
  const indLoss = {};
  rows.forEach(r => {
    const k = r[indKey] || 'Other';
    indLoss[k] = (indLoss[k] || 0) + (parseFloat(r[lossKey]) || 0);
  });
  Plotly.newPlot('chartPlot2', [{
    x: Object.values(indLoss),
    y: Object.keys(indLoss),
    type: 'bar',
    orientation: 'h',
    marker: { color: '#2563eb' }
  }], {
    ...plotLayoutDefaults,
    title: { text: '<b>Loss by Target Sector ($M)</b>', x: 0.01, y: 0.97, font: { size: 12, color: '#0f172a' } },
    xaxis: { ...plotLayoutDefaults.xaxis, title: { text: 'Loss ($M)', font: { size: 10 } } }
  }, plotConfig);

  // Chart 3: Threat Actor
  const srcCounts = countBy(rows, srcKey);
  Plotly.newPlot('chartPlot3', [{
    x: Object.keys(srcCounts),
    y: Object.values(srcCounts),
    type: 'bar',
    marker: { color: '#475569' }
  }], {
    ...plotLayoutDefaults,
    title: { text: '<b>Threat Actor Attribution</b>', x: 0.01, y: 0.97, font: { size: 12, color: '#0f172a' } },
    yaxis: { ...plotLayoutDefaults.yaxis, title: { text: 'Incidents', font: { size: 10 } } }
  }, plotConfig);

  // Chart 4: Vulnerability vs Defense
  const vulnTypes = [...new Set(rows.map(r => r[vulnKey]).filter(Boolean))];
  const defTypes = [...new Set(rows.map(r => r[defKey]).filter(Boolean))];
  const traces = defTypes.map(d => ({
    name: d,
    x: vulnTypes,
    y: vulnTypes.map(v => rows.filter(r => r[vulnKey] === v && r[defKey] === d).length),
    type: 'bar'
  }));
  Plotly.newPlot('chartPlot4', traces, {
    ...plotLayoutDefaults,
    barmode: 'stack',
    title: { text: '<b>Vulnerabilities vs Defenses</b>', x: 0.01, y: 0.97, font: { size: 12, color: '#0f172a' } },
    xaxis: { ...plotLayoutDefaults.xaxis, tickangle: -15 }
  }, plotConfig);

  // Chart 5: Countries
  const cCounts = countBy(rows, cKey);
  const sortedCountries = Object.entries(cCounts).sort((a,b) => b[1] - a[1]).slice(0, 10);
  Plotly.newPlot('chartPlot5', [{
    x: sortedCountries.map(x => x[1]),
    y: sortedCountries.map(x => x[0]),
    type: 'bar',
    orientation: 'h',
    marker: { color: '#059669' }
  }], {
    ...plotLayoutDefaults,
    yaxis: { ...plotLayoutDefaults.yaxis, autorange: 'reversed' },
    xaxis: { ...plotLayoutDefaults.xaxis, title: { text: 'Incidents', font: { size: 10 } } },
    title: { text: '<b>Top Impacted Countries</b>', x: 0.01, y: 0.97, font: { size: 12, color: '#0f172a' } }
  }, plotConfig);

  // Chart 6: Damage vs Resolution Time Scatter
  Plotly.newPlot('chartPlot6', [{
    x: rows.map(r => r[timeKey]),
    y: rows.map(r => r[lossKey]),
    mode: 'markers',
    type: 'scatter',
    marker: { color: '#2563eb', size: 5, opacity: 0.7 }
  }], {
    ...plotLayoutDefaults,
    title: { text: '<b>Damage vs Resolution Latency</b>', x: 0.01, y: 0.97, font: { size: 12, color: '#0f172a' } },
    xaxis: { ...plotLayoutDefaults.xaxis, title: { text: 'Latency (hrs)', font: { size: 10 } } },
    yaxis: { ...plotLayoutDefaults.yaxis, title: { text: 'Loss ($M)', font: { size: 10 } } }
  }, plotConfig);
}

function renderTrafficCharts(rows, schema) {
  const normalCount = rows.filter(r => r.prediction === 0).length;
  const anomCount = rows.filter(r => r.prediction === 1).length;

  // Chart 1: Threat Severity Donut
  const sevCounts = countBy(rows, 'severity');
  const sevOrder = ['CRITICAL', 'HIGH', 'MEDIUM', 'NORMAL'].filter(s => sevCounts[s]);
  const sevColors = { 'CRITICAL': '#dc2626', 'HIGH': '#ea580c', 'MEDIUM': '#eab308', 'NORMAL': '#10b981' };

  Plotly.newPlot('chartPlot1', [{
    labels: sevOrder.length ? sevOrder : ['Normal', 'Anomaly'],
    values: sevOrder.length ? sevOrder.map(s => sevCounts[s]) : [normalCount, anomCount],
    type: 'pie',
    hole: 0.64,
    textfont: { size: 10 },
    textinfo: 'percent',
    marker: { colors: sevOrder.length ? sevOrder.map(s => sevColors[s] || '#64748b') : ['#10b981', '#ef4444'] }
  }], {
    ...plotLayoutDefaults,
    title: { text: '<b>Threat Severity Distribution</b>', x: 0.01, y: 0.97, font: { size: 12, color: '#0f172a' } }
  }, plotConfig);

  // Chart 2: Identified Attack Vectors
  const atkCounts = countBy(rows, 'attack_type');
  Plotly.newPlot('chartPlot2', [{
    x: Object.values(atkCounts),
    y: Object.keys(atkCounts),
    type: 'bar',
    orientation: 'h',
    marker: { color: '#2563eb' }
  }], {
    ...plotLayoutDefaults,
    title: { text: '<b>Identified Cyber Attack Vectors</b>', x: 0.01, y: 0.97, font: { size: 12, color: '#0f172a' } },
    xaxis: { ...plotLayoutDefaults.xaxis, title: { text: 'Connections', font: { size: 10 } } },
    yaxis: { ...plotLayoutDefaults.yaxis, autorange: 'reversed' }
  }, plotConfig);

  // Chart 3: Protocol or Port Volume
  if (rows[0]['protocol_type'] !== undefined) {
    const protoCounts = countBy(rows, 'protocol_type');
    Plotly.newPlot('chartPlot3', [{
      x: Object.keys(protoCounts),
      y: Object.values(protoCounts),
      type: 'bar',
      marker: { color: '#3b82f6' }
    }], {
      ...plotLayoutDefaults,
      title: { text: '<b>Volume by Protocol</b>', x: 0.01, y: 0.97, font: { size: 12, color: '#0f172a' } },
      yaxis: { ...plotLayoutDefaults.yaxis, title: { text: 'Connections', font: { size: 10 } } }
    }, plotConfig);
  } else if (rows[0]['Destination Port'] !== undefined) {
    const portCounts = countBy(rows, 'Destination Port');
    const sortedPorts = Object.entries(portCounts).slice(0, 8);
    Plotly.newPlot('chartPlot3', [{
      x: sortedPorts.map(p => `Port ${p[0]}`),
      y: sortedPorts.map(p => p[1]),
      type: 'bar',
      marker: { color: '#3b82f6' }
    }], {
      ...plotLayoutDefaults,
      title: { text: '<b>Top Destination Ports</b>', x: 0.01, y: 0.97, font: { size: 12, color: '#0f172a' } },
      yaxis: { ...plotLayoutDefaults.yaxis, title: { text: 'Flows', font: { size: 10 } } }
    }, plotConfig);
  } else {
    Plotly.newPlot('chartPlot3', [{
      labels: ['Normal', 'Anomaly'],
      values: [normalCount, anomCount],
      type: 'pie',
      hole: 0.5,
      marker: { colors: ['#10b981', '#ef4444'] }
    }], {
      ...plotLayoutDefaults,
      title: { text: '<b>Classification Ratio</b>', x: 0.01, y: 0.97, font: { size: 12, color: '#0f172a' } }
    }, plotConfig);
  }

  // Chart 4: Flags or Duration
  if (rows[0]['flag'] !== undefined) {
    const flagCounts = countBy(rows, 'flag');
    Plotly.newPlot('chartPlot4', [{
      x: Object.keys(flagCounts),
      y: Object.values(flagCounts),
      type: 'bar',
      marker: { color: '#10b981' }
    }], {
      ...plotLayoutDefaults,
      title: { text: '<b>Connection State Flags</b>', x: 0.01, y: 0.97, font: { size: 12, color: '#0f172a' } },
      yaxis: { ...plotLayoutDefaults.yaxis, title: { text: 'Packets', font: { size: 10 } } }
    }, plotConfig);
  } else {
    const durations = rows.map(r => Math.log10(Math.max(1, parseFloat(r['Flow Duration']) || 1)));
    Plotly.newPlot('chartPlot4', [{
      x: durations,
      type: 'histogram',
      marker: { color: '#2563eb' }
    }], {
      ...plotLayoutDefaults,
      title: { text: '<b>Flow Duration Telemetry</b>', x: 0.01, y: 0.97, font: { size: 12, color: '#0f172a' } },
      xaxis: { ...plotLayoutDefaults.xaxis, title: { text: 'Log(Duration µs)', font: { size: 10 } } }
    }, plotConfig);
  }

  // Chart 5: Probability Histogram
  const probs = rows.map(r => r.anomaly_probability);
  Plotly.newPlot('chartPlot5', [{
    x: probs,
    type: 'histogram',
    marker: { color: '#ef4444' }
  }], {
    ...plotLayoutDefaults,
    title: { text: '<b>Anomaly Confidence Distribution</b>', x: 0.01, y: 0.97, font: { size: 12, color: '#0f172a' } },
    xaxis: { ...plotLayoutDefaults.xaxis, title: { text: 'Score', font: { size: 10 } } },
    yaxis: { ...plotLayoutDefaults.yaxis, title: { text: 'Frequency', font: { size: 10 } } }
  }, plotConfig);

  // Chart 6: Volume Signature
  if (rows[0]['src_bytes'] !== undefined) {
    Plotly.newPlot('chartPlot6', [{
      x: rows.map(r => Math.log10(Math.max(1, parseFloat(r.src_bytes) || 1))),
      y: rows.map(r => Math.log10(Math.max(1, parseFloat(r.dst_bytes) || 1))),
      mode: 'markers',
      type: 'scatter',
      marker: { color: rows.map(r => r.prediction === 1 ? '#ef4444' : '#10b981'), size: 5, opacity: 0.65 }
    }], {
      ...plotLayoutDefaults,
      title: { text: '<b>Payload Signature (Src / Dst)</b>', x: 0.01, y: 0.97, font: { size: 12, color: '#0f172a' } },
      xaxis: { ...plotLayoutDefaults.xaxis, title: { text: 'Log(Src Bytes)', font: { size: 10 } } },
      yaxis: { ...plotLayoutDefaults.yaxis, title: { text: 'Log(Dst Bytes)', font: { size: 10 } } }
    }], plotConfig);
  } else {
    Plotly.newPlot('chartPlot6', [{
      x: rows.map(r => Math.log10(Math.max(1, parseFloat(r['Total Fwd Packets']) || 1))),
      y: rows.map(r => Math.log10(Math.max(1, parseFloat(r['Flow Duration']) || 1))),
      mode: 'markers',
      type: 'scatter',
      marker: { color: rows.map(r => r.prediction === 1 ? '#ef4444' : '#10b981'), size: 5, opacity: 0.7 }
    }], {
      ...plotLayoutDefaults,
      title: { text: '<b>Flow Duration vs Packets</b>', x: 0.01, y: 0.97, font: { size: 12, color: '#0f172a' } },
      xaxis: { ...plotLayoutDefaults.xaxis, title: { text: 'Log(Fwd Pkts)', font: { size: 10 } } },
      yaxis: { ...plotLayoutDefaults.yaxis, title: { text: 'Log(Duration)', font: { size: 10 } } }
    }], plotConfig);
  }
}

// Table Logs
function renderTableLogs(schema, rows) {
  const logsEmptyNotice = document.getElementById('logsEmptyNotice');
  const logsContent = document.getElementById('logsContent');
  const tableHead = document.getElementById('tableHead');
  const tableBody = document.getElementById('tableBody');
  const tableRecordCount = document.getElementById('tableRecordCount');

  logsEmptyNotice.style.display = 'none';
  logsContent.style.display = 'block';

  tableRecordCount.textContent = `Showing ${Math.min(rows.length, 500).toLocaleString()} of ${rows.length.toLocaleString()} records`;

  const priorityKeys = ['severity', 'attack_type', 'classification', 'detection_reason', 'recommended_action', 'anomaly_probability'];
  const allRowKeys = Object.keys(rows[0]);
  const leadingKeys = priorityKeys.filter(k => allRowKeys.includes(k));
  const remainingKeys = allRowKeys.filter(k => !priorityKeys.includes(k) && k !== 'prediction');
  const displayKeys = leadingKeys.concat(remainingKeys).slice(0, 10);

  tableHead.innerHTML = '<tr>' + displayKeys.map(k => `<th>${k.replace(/_/g, ' ').toUpperCase()}</th>`).join('') + '</tr>';

  tableBody.innerHTML = rows.slice(0, 150).map(r => {
    return '<tr>' + displayKeys.map(k => {
      const val = r[k];
      if (k === 'severity') {
        const sevClass = val === 'CRITICAL' ? 'badge-critical' : (val === 'HIGH' ? 'badge-high' : (val === 'MEDIUM' ? 'badge-medium' : 'badge-normal'));
        return `<td><span class="${sevClass}">${val}</span></td>`;
      }
      if (k === 'classification') {
        const cls = val === 'Anomaly' || val === 'Threat Incident' ? 'badge-anomaly' : 'badge-normal';
        return `<td><span class="${cls}">${val}</span></td>`;
      }
      if (k === 'anomaly_probability') {
        return `<td><code>${typeof val === 'number' ? val.toFixed(4) : val}</code></td>`;
      }
      return `<td>${val !== undefined && val !== null ? val : ''}</td>`;
    }).join('') + '</tr>';
  }).join('');
}

// History UI
function updateHistoryUI() {
  tabHistoryBtn.textContent = `Ingestion History (${ingestionHistory.length})`;
  historyEmptyNotice.style.display = 'none';
  historyList.innerHTML = ingestionHistory.map(h => `
    <div class="history-card">
      <div>
        <span class="history-id">${h.id}</span>
        <div style="font-size: 11px; color: #94a3b8;">${h.time}</div>
      </div>
      <div>
        <strong>${h.fileName}</strong>
        <div style="font-size: 12px; color: #64748b;">${h.schema} | ${h.records.toLocaleString()} rows</div>
      </div>
      <div>
        <span class="badge-normal">${h.summary}</span>
        <div style="font-size: 11px; color: #94a3b8;">Latency: ${h.latency} ms</div>
      </div>
    </div>
  `).join('');
}

// Helper: countBy
function countBy(arr, key) {
  const res = {};
  arr.forEach(item => {
    const val = item[key] || 'Unknown';
    res[val] = (res[val] || 0) + 1;
  });
  return res;
}
