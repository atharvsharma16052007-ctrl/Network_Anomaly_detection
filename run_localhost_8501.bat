@echo off
title Netshield Cyber Telemetry Console
echo ========================================================
echo   Launching Netshield on http://localhost:8501 ...
echo ========================================================
streamlit run streamlit_app.py --server.port 8501
pause
