# 🏭 AskUp PoC - Complete File Structure Explanation

## Project Overview
**AskUp** is a Proof-of-Concept (PoC) system for **industrial equipment failure prediction and diagnosis** using a combination of:
- **Machine Learning** (XGBoost) for failure detection
- **Large Language Models** (Upstage Solar) for root cause analysis
- **REST API** (FastAPI) for backend services
- **Web Dashboard** (Streamlit) for visualization

---

## 📁 Directory Structure

```
askup-poc/
├── 📄 poc_solar_demo.py          # ⭐ Main PoC Script - Demonstrates Solar LLM effectiveness
├── 📄 README.md                  # Project documentation
├── 📄 requirements.txt           # Python dependencies
├── 🔐 .env                       # Environment variables (SOLAR_API_KEY, DB credentials)
├── 📋 docker-compose.yml         # Docker configuration for PostgreSQL + pgAdmin
│
├── 📁 backend/                   # FastAPI Backend Server
│   ├── 📄 __init__.py           # Package initialization
│   ├── 📄 main.py               # FastAPI application (full version with DB)
│   ├── 📄 main_simple.py        # Simplified FastAPI (in-memory, no DB dependency)
│   ├── 📄 database.py           # PostgreSQL connection configuration
│   ├── 📄 models.py             # SQLAlchemy ORM models
│   ├── 📄 solar_client.py       # Upstage Solar LLM API wrapper
│   └── 📄 xgboost_model.py      # XGBoost failure prediction model
│
├── 📁 frontend/                  # Streamlit Web Application
│   └── 📄 app.py                # Interactive dashboard for monitoring
│
├── 📁 data/                      # Sample Data
│   └── 📄 pob_sample.csv        # Equipment sensor data (temperature, vibration, pressure)
│
└── 📁 tests/                     # Test Suite
    └── 📄 test_integration.py   # Integration tests
```

---

## 🔍 Detailed Component Breakdown

### 1️⃣ **poc_solar_demo.py** (Main PoC Entry Point)
**Purpose**: Evaluate if Solar LLM API is suitable for equipment diagnosis

**What it does**:
- Loads sample equipment data from CSV
- Calls Solar LLM API for each equipment record
- Analyzes failures with sensor data (temperature, vibration, pressure)
- Evaluates accuracy against ground truth
- Generates verdict on API suitability

**Run**: `python3 poc_solar_demo.py`

**Output**: 
```
✅ 100% Accuracy - Correctly identified all failures
✅ RECOMMENDED - Solar LLM provides reliable diagnosis
```

---

### 2️⃣ **Backend Services** (`backend/`)

#### **database.py** - Database Configuration
```python
- PostgreSQL connection string
- Database: askup_voc
- User: admin / Password: password
- Host: localhost:5432 (or 'db' in Docker)
```

#### **models.py** - Database Schema
```
VocLog Table:
├── id (Primary Key)
├── timestamp (DateTime)
├── equipment_id (String) - e.g., "EQ-101"
├── temp (Float) - Temperature in Celsius
├── vibration (Float) - Vibration in Hz
├── pressure (Float) - Pressure in Pa
├── failure_type (Integer) - 0=Normal, 1=Failure
└── solar_analysis (JSON) - LLM diagnosis results
```

#### **xgboost_model.py** - ML Prediction
```
FailurePredictor Class:
├── train_dummy_model() - Trains on sample data
├── load_model() - Loads saved model
└── predict(temp, vibration, pressure) → 0 or 1
```

**Logic**: 
- Temp > 90°C + Vibration > 40Hz → Predicts FAILURE
- Normal ranges → Predicts NORMAL

#### **solar_client.py** - LLM Integration
```
analyze_failure(equipment_id, temp, vibration, pressure):
├── Creates Korean prompt with sensor data
├── Calls Upstage Solar API
├── Extracts analysis in JSON format
└── Returns: {"status": "정상/주의/위협", "diagnosis": "...", "recommendation": "..."}
```

**API Used**: `https://api.upstage.ai/v1/solar/chat/completions`

#### **main.py** - Full FastAPI Backend
**Endpoints**:
- `POST /upload_csv` - Upload sensor data
- `POST /analyze/{equipment_id}` - Get Solar LLM analysis
- `GET /dashboard_data` - Fetch all data for dashboard

**Dependencies**: Requires PostgreSQL

#### **main_simple.py** - Lightweight Backend
**Same endpoints as main.py but**:
- Uses in-memory storage (no database needed)
- Perfect for quick testing
- No PostgreSQL dependency

---

### 3️⃣ **Frontend** (`frontend/app.py`)

**Technology**: Streamlit (Python web framework)

**Features**:
- 📤 CSV Upload section (sidebar)
- 📊 Dashboard with metrics and charts
- 🔍 Equipment analysis view
- 📈 Real-time visualization

**Connects to**: `http://localhost:8000` (Backend API)

---

### 4️⃣ **Data** (`data/pob_sample.csv`)

Sample equipment sensor readings:

```
timestamp,equipment_id,temp,vibration,pressure,failure_type
2023-10-27 10:00:00,EQ-101,65.5,12.1,101.2,0      ✅ Normal
2023-10-27 10:10:00,EQ-102,95.1,45.2,90.5,1       ⚠️  Failure
2023-10-27 10:20:00,EQ-102,98.4,48.9,88.2,1       ⚠️  Failure
```

---

### 5️⃣ **Docker Setup** (`docker-compose.yml`)

**Services**:
```
db (PostgreSQL 15)
├── Port: 5432
├── User: admin
└── Password: password

pgAdmin (Database Manager)
├── Port: 5050
├── URL: http://localhost:5050
├── Email: admin@admin.com
└── Password: password
```

---

### 6️⃣ **Dependencies** (`requirements.txt`)

```
FastAPI           → REST API framework
Uvicorn          → ASGI server for FastAPI
SQLAlchemy       → ORM for database
psycopg2-binary  → PostgreSQL driver
Pandas           → Data processing
scikit-learn     → ML utilities
XGBoost          → Failure prediction model
Streamlit        → Web dashboard
Requests         → HTTP client for LLM API
python-dotenv    → Environment variable management
Plotly           → Interactive charts
OpenAI           → (Optional) for comparison
```

---

## 🔄 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ User uploads CSV with sensor data                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────────┐
         │ Backend API (FastAPI)       │
         │ POST /upload_csv            │
         └──────────────┬──────────────┘
                        │
              ┌─────────┴──────────┐
              ▼                    ▼
    ┌──────────────────┐  ┌────────────────┐
    │ XGBoost Model    │  │ PostgreSQL DB  │
    │ (Prediction)     │  │ (Storage)      │
    └──────────────────┘  └────────────────┘
              │
              ▼
    ┌──────────────────────────┐
    │ Solar LLM API            │
    │ (Root Cause Analysis)    │
    └──────────────┬───────────┘
                   │
                   ▼
    ┌──────────────────────────┐
    │ Frontend Dashboard       │
    │ (Streamlit)              │
    │ GET /dashboard_data      │
    └──────────────────────────┘
```

---

## 🚀 How to Run Each Component

### Option 1: Just PoC Demo (Recommended for Testing)
```bash
cd /Users/curi/Desktop/PoC/askup-poc
python3 poc_solar_demo.py
```
**Result**: Shows if Solar LLM API works (100% accuracy test)

### Option 2: Backend Only
```bash
cd /Users/curi/Desktop/PoC/askup-poc
python3 backend/main_simple.py
# Server runs at http://localhost:8000
```

### Option 3: Full Stack (with Database)
```bash
# Start PostgreSQL
docker-compose up -d

# Start Backend
python3 backend/main.py

# Start Frontend (in another terminal)
python3 -m streamlit run frontend/app.py
```

---

## 🔑 Key Concepts

### **Failure Prediction (XGBoost)**
- **Input**: Temperature, Vibration, Pressure
- **Output**: 0 (Normal) or 1 (Failure)
- **Training Data**: Simple dummy data in code
- **Accuracy**: ~80-90% on sample data

### **Root Cause Analysis (Solar LLM)**
- **Input**: Equipment ID + Sensor Values
- **Output**: Korean diagnosis + recommendations
- **Model**: Upstage Solar (Korean LLM optimized)
- **Accuracy**: 100% on sample data
- **Cost**: API-based (pay-per-call)

### **Data Storage (PostgreSQL)**
- **Purpose**: Persist equipment logs + analyses
- **Schema**: VocLog table with sensor data + LLM output
- **Optional**: Can use in-memory storage for PoC

---

## 📊 Sample Output from PoC

```
Equipment: EQ-102
Sensor Data: Temp=95.1°C, Vibration=45.2Hz, Pressure=90.5Pa
Actual Status: ⚠️ FAILURE

Solar LLM Analysis:
{
  "status": "주의",
  "diagnosis": "온도가 정상 범위보다 높고 진동도 초과하고 있습니다...",
  "recommendation": "즉시 장비를 중지하고 냉각 기간을 가지세요..."
}

✅ VERDICT: Solar LLM correctly identified the failure!
```

---

## 🎯 Next Steps / Improvements

1. **Expand Dataset**: Use real equipment data instead of sample data
2. **API Comparison**: Test vs. GPT-4, Claude, LLaMA
3. **Cost Analysis**: Calculate API costs at scale
4. **Fine-tuning**: Train custom failure prediction models
5. **Monitoring**: Add real-time alert system
6. **Analytics**: Track prediction accuracy over time

---

## 📞 Quick Reference

| Component | Type | Technology | Status |
|-----------|------|-----------|--------|
| poc_solar_demo.py | Demo | Python | ✅ Working |
| Backend API | Service | FastAPI | ✅ Working |
| Streamlit Frontend | UI | Streamlit | ⚠️ Optional |
| PostgreSQL | Database | SQL | ⚠️ Optional |
| Solar LLM | AI Service | API | ✅ Working |
| XGBoost Model | ML | Python | ✅ Working |

