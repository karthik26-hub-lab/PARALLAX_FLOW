@echo off
title ParallaxFlow OCR - Production Handwriting Engine
echo ========================================================
echo  ParallaxFlow OCR - Production Handwriting Engine
echo ========================================================
echo.
echo Starting backend server on http://127.0.0.1:8000...

set PYTHONIOENCODING=utf-8

start "" "http://127.0.0.1:8000"

.venv\Scripts\uvicorn.exe backend.main:app --host 127.0.0.1 --port 8000
