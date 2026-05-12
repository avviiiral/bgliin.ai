# 🏭 Factory Monitoring System (Full Stack: Django + YOLO + Angular)

A **real-time, production-ready factory monitoring system** that uses CCTV feeds, YOLO-based detection, and a live dashboard to track production across multiple stations.

---

# 🚀 OVERVIEW

This system enables:

* 🎥 Multi-camera monitoring (RTSP CCTV)
* 🤖 YOLOv8-based detection & counting
* 📊 CSV-based production logging (no DB dependency)
* 🌐 Django REST API backend
* 🎯 Angular dashboard (Bagla UI)
* 📺 Live video streaming (MJPEG)
* 📈 Efficiency & production analytics

---

# 🧱 TECH STACK

### Backend

* Python 3.10+
* Django
* Django REST Framework
* OpenCV
* YOLOv8 (Ultralytics)
* Multiprocessing

### Frontend

* Angular
* ApexCharts (for analytics)
* Bagla UI (custom dashboard)

---

# 📁 PROJECT STRUCTURE

```bash
factory-monitoring-system/
│
├── backend/
│   ├── core/
│   │   ├── config.py
│   │   ├── camera_manager.py
│   │   ├── counter.py
│   │   ├── inference.py
│   │   ├── csv_writer.py
│   │   ├── system_controller.py
│   │   ├── logger.py
│   │
│   ├── apps/
│   │   ├── cameras/
│   │   ├── analytics/
│   │
│   ├── django_project/
│   ├── manage.py
│   ├── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── angular.json
│   ├── package.json
│
└── README.md
```

---

# ⚙️ BACKEND SETUP (DJANGO)

## 1️⃣ Setup Environment

```bash
cd backend
python -m venv venv
venv\Scripts\activate
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Run Migrations

```bash
python manage.py migrate
```

---

## 4️⃣ Start Backend Server

```bash
python manage.py runserver
```

---

## 🔍 Test Backend APIs

```
http://127.0.0.1:8000/api/cameras/
http://127.0.0.1:8000/api/stats/
http://127.0.0.1:8000/api/history/cam1/
http://127.0.0.1:8000/api/efficiency/cam1/
http://127.0.0.1:8000/api/stream/cam1/
```

---

# 🎥 CAMERA CONFIGURATION

## 📄 `backend/core/config.py`

```python
CAMERAS = {
    "cam1": {
        "ip": "192.168.1.193",
        "name": "AIR WASHING",
        "mode": "x",
        "pos": 1100,
        "dir": "lr",
        "multiplier": 1
    }
}
```

---

# 🧪 TEST WITHOUT CAMERA (DUMMY MODE)

If you are not connected to camera network:

```python
import numpy as np

frame = np.zeros((FRAME_H, FRAME_W, 3), dtype=np.uint8)
cv2.putText(frame, cam_id, (50,100),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
```

---

# 📊 CSV OUTPUT

File: `production_hourly.csv`

```
Date, Time Slot, AIR WASHING
2026-04-22, 10:00-10:59, 120
```

---

# 🌐 FRONTEND SETUP (ANGULAR)

## 1️⃣ Install Dependencies

```bash
cd frontend
npm install
npm i --f
```

---

## 2️⃣ Run Frontend

```bash
npm start
```

---

## 🌍 Open Dashboard

```
http://localhost:4200/
```

---

# 🔗 FRONTEND API CONFIG

## 📄 `api.service.ts`

```ts
const BASE = 'http://127.0.0.1:8000/api';
```

---

# 📺 LIVE STREAMING

```html
<img [src]="'http://127.0.0.1:8000/api/stream/' + cameraId">
```

---

# 🧠 SYSTEM ARCHITECTURE

```
CCTV Cameras
     ↓
Capture Workers (multiprocessing)
     ↓
YOLO Inference (GPU optional)
     ↓
Line Crossing Counter
     ↓
CSV Storage
     ↓
Django APIs
     ↓
Angular Dashboard
```

---

# 📜 LOGGING

Logs stored in:

```
system.log
```

Usage:

```python
from core.logger import logger

logger.info("System started")
logger.error("Camera failed")
```

---

# ⚠️ COMMON ISSUES

| Issue                  | Solution                     |
| ---------------------- | ---------------------------- |
| No module named django | Activate virtual environment |
| Stream not working     | Connect to camera network    |
| Empty dashboard        | Check `/api/cameras/`        |
| Torch DLL error        | Install CPU version          |
| CORS error             | Enable in Django settings    |

---

# 🧱 PRODUCTION DEPLOYMENT

### Recommended Setup

```
Angular → Nginx → Django → Core Engine
```

### Avoid:

* Django dev server in production ❌

---

# 🐳 DOCKER (OPTIONAL)

```bash
docker build -t factory-monitor .
docker run -p 8000:8000 factory-monitor
```

---

# 🔥 FUTURE IMPROVEMENTS

* ⚡ GPU acceleration (CUDA)
* 📉 Downtime detection
* 🚨 Alert system (email / sound)
* 📊 Shift-based production targets
* 📡 WebSocket streaming

---

# 🏁 CURRENT STATUS

```
✔ Backend ready
✔ Core AI engine running
✔ CSV analytics working
✔ Angular dashboard live
✔ Live streaming working
✔ Multi-camera support enabled
✔ Production architecture complete
```

---

# 👨‍💻 AUTHOR

**Aviral Goyal**

AI / ML / Computer Vision Systems

📧 Email: [aviralgoyal739@gmail.com](mailto:aviralgoyal739@gmail.com)

🔗 LinkedIn: https://www.linkedin.com/in/avviiiral

---

# 📌 FINAL NOTE

```
✔ Real-time
✔ Scalable
✔ Industrial-grade
✔ Production-ready
```

---

# ⭐ If you found this useful, consider starring the repo!
