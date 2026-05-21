# BGLIIN.AI – Installation & Setup Guide

## Overview
BGLIIN.AI is a production monitoring and analytics system built using:

- Backend: Django + Python
- Frontend: Angular
- AI/Detection: YOLOv8 + OpenCV + PyTorch
- Database/Data Source: CSV-based production data

This guide explains how to:

1. Install backend dependencies
2. Install frontend dependencies
3. Run backend server
4. Run frontend server
5. Configure CUDA/GPU support
6. Fix common issues

---

# Project Structure

```bash
bgliin.ai/
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── django_project/
│   ├── apps/
│   ├── core/
│   ├── production_hourly.csv
│   └── targets.csv
│
├── frontend/
│   ├── angular.json
│   ├── package.json
│   ├── src/
│   └── package-lock.json
│
└── readme.md
```

---

# System Requirements

## Recommended

| Component | Recommended |
|---|---|
| OS | Windows 10/11 |
| Python | Python 3.10 or 3.11 |
| Node.js | Node.js 18 LTS |
| RAM | Minimum 16 GB |
| GPU | NVIDIA GPU with CUDA support |
| CUDA | CUDA 12.1 |

---

# Step 1 — Install Required Software

## Install Python

Download and install Python:

urlPython Official Websitehttps://www.python.org/downloads/

During installation:

- Enable `Add Python to PATH`
- Click `Install Now`

Verify installation:

```bash
python --version
```

---

## Install Node.js

Download Node.js 18 LTS:

urlNode.js Official Websitehttps://nodejs.org/en/download

Verify installation:

```bash
node -v
npm -v
```

---

## Install Git

Download Git:

urlGit Official Websitehttps://git-scm.com/downloads

Verify installation:

```bash
git --version
```

---

# Step 2 — Extract Project

Extract the ZIP file.

Example:

```bash
D:\bagla.ai\bgliin.ai
```

Open terminal inside project folder.

---

# Backend Setup (Django + YOLO)

# Step 3 — Open Backend Folder

```bash
cd backend
```

---

# Step 4 — Create Virtual Environment

## Windows

```bash
python -m venv venv
```

Activate virtual environment:

```bash
venv\Scripts\activate
```

You should see:

```bash
(venv)
```

---

# Step 5 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:

- Django
- OpenCV
- PyTorch
- YOLOv8
- NumPy
- Pandas
- FastAPI
- Ultralytics
- All required backend libraries

---

# Step 6 — Install CUDA PyTorch (GPU Recommended)

If using NVIDIA GPU:

```bash
pip uninstall torch torchvision torchaudio -y
```

Install CUDA 12.1 version:

```bash
pip install torch==2.5.1+cu121 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Verify GPU:

```bash
python
```

Then run:

```python
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
```

Expected output:

```python
True
NVIDIA RTX xxxx
```

Exit Python:

```python
exit()
```

---

# Step 7 — Run Django Backend

Run migrations:

```bash
python manage.py migrate
```

Start backend server:

```bash
python manage.py runserver
uvicorn django_project.asgi:application --host 0.0.0.0 --port 8000
```

Backend should run on:

```bash
http://127.0.0.1:8000/
```

---

# Step 8 — Run YOLO Production Monitoring System

Inside backend folder:

```bash
python core/run_system.py
```

This starts:

- Camera streams
- YOLO detection
- Counting system
- CSV updates
- Production analytics

---

# Frontend Setup (Angular)

Open a NEW terminal.

---

# Step 9 — Open Frontend Folder

```bash
cd frontend
```

---

# Step 10 — Install Angular Dependencies

```bash
npm install
```

This installs:

- Angular
- PrimeNG
- Bootstrap
- ApexCharts
- Chart.js
- RxJS
- All frontend dependencies

---

# Step 11 — Start Angular Frontend

```bash
ng serve
```

OR

```bash
npm start
```

Frontend will run on:

```bash
http://localhost:4200/
```

---

# Full Startup Flow

## Terminal 1 — Backend

```bash
cd backend
venv\Scripts\activate
python manage.py runserver
```

---

## Terminal 2 — YOLO System

```bash
cd backend
venv\Scripts\activate
python core/run_system.py
```

---

## Terminal 3 — Frontend

```bash
cd frontend
npm start
```

---

# API Endpoints

## Dashboard APIs

```bash
/api/dashboard/
/api/stations/
/api/camera/<camera_id>/
/api/camera/<camera_id>/calendar/
/api/camera/<camera_id>/history/
```

---

# CSV Files

## production_hourly.csv

Stores:

- Production count
- Hourly output
- Shift-wise production
- Historical production data

---

## targets.csv

Stores:

- Camera targets
- Cycle time
- Production goals
- Expected hourly output

---

# Common Commands

## Install New Python Package

```bash
pip install package_name
```

Update requirements:

```bash
pip freeze > requirements.txt
```

---

## Install New Frontend Package

```bash
npm install package-name
```

---

## Create Django Admin User

```bash
python manage.py createsuperuser
```

---

# Common Errors & Fixes

# 1. torch DLL Error

Example:

```bash
OSError: [WinError 126]
```

Fix:

- Install CUDA compatible PyTorch
- Install Microsoft Visual C++ Redistributable

Download:

urlMicrosoft Visual C++ Redistributablehttps://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist

---

# 2. ng Command Not Found

Install Angular CLI globally:

```bash
npm install -g @angular/cli
```

Verify:

```bash
ng version
```

---

# 3. Port Already in Use

## Backend Port Issue

```bash
python manage.py runserver 8001
```

---

## Frontend Port Issue

```bash
ng serve --port 4201
```

---

# 4. CUDA Not Detected

Check:

```bash
nvidia-smi
```

If command fails:

- Install NVIDIA drivers
- Install CUDA Toolkit

CUDA Download:

urlNVIDIA CUDA Toolkithttps://developer.nvidia.com/cuda-downloads

---

# 5. Angular Build Error

Delete:

```bash
node_modules
package-lock.json
```

Reinstall:

```bash
npm install
```

---

# Recommended Development Workflow

1. Start Django backend
2. Start YOLO detection system
3. Start Angular frontend
4. Open dashboard in browser
5. Monitor production data live

---

# Production Deployment Notes

For production deployment use:

- Nginx
- Gunicorn/Uvicorn
- PM2 for frontend
- Docker (optional)
- GPU-enabled system for YOLO

---

# Performance Recommendations

## For Real-Time CCTV Monitoring

Recommended:

- RTX 4060 or higher
- Minimum 8 GB VRAM
- SSD storage
- 32 GB RAM
- Dedicated AI workstation

---

# Useful Commands

## Backend

```bash
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
```

---

## Frontend

```bash
npm install
npm start
ng serve
ng build
```

---

# Final URLs

## Frontend

```bash
http://localhost:4200
```

## Backend

```bash
http://127.0.0.1:8000
```

---

# Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Angular 15 |
| Backend | Django 5 |
| AI Model | YOLOv8 |
| Computer Vision | OpenCV |
| Deep Learning | PyTorch |
| Charts | ApexCharts + Chart.js |
| Data | CSV-based analytics |

---

# Notes

- Always activate virtual environment before backend work.
- Run backend and frontend in separate terminals.
- GPU is highly recommended for multi-camera processing.
- CSV files update automatically during production monitoring.
- Use SSD storage for better video processing performance.

---

# Author

Aviral Goyal

LinkedIn:

urlAviral Goyal LinkedInhttps://www.linkedin.com/in/avviiiral

