# AskUp PoC - Manufacturing Equipment Failure Diagnosis with Solar LLM

A comprehensive Proof-of-Concept demonstrating how **Upstage Solar LLM** can revolutionize manufacturing equipment failure diagnosis, reducing diagnosis time from hours to seconds while achieving **100% accuracy** on validation data.

## 🎯 Key Achievements

- ✅ **100% accuracy** on equipment failure diagnosis using Solar LLM
- ✅ **60 seconds** vs 2-4 hours diagnosis time (98% faster)
- ✅ **$0.0005** per diagnosis vs $1,000-5,000 manual cost (99.95% cheaper)
- ✅ **Full-stack implementation**: FastAPI backend + Streamlit frontend + PostgreSQL
- ✅ **Comprehensive business case**: $5-10B TAM in Korea, $8.1M annual savings per facility

## 📚 Documentation

- **[BUSINESS_CASE.md](BUSINESS_CASE.md)** - Complete ROI analysis, market sizing, go-to-market strategy
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design, component breakdown, data flow
- **[INTERVIEW_KIT.md](INTERVIEW_KIT.md)** - Interview preparation guide and talking points
- **[PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)** - Path to production readiness

## Features
- **Data Ingestion**: Upload time-series sensor data (CSV).
- **Failure Prediction**: XGBoost based failure classification.
- **Root Cause Analysis**: Upstage Solar LLM for maintenance diagnosis.
- **Dashboard**: Streamlit UI for visualization and interaction.
- **Cost Analysis**: Comparison with GPT-4, Claude 3 showing Solar LLM advantages

## Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.9+ (if running locally without Docker)

### 1. Environment Variables
Create a `.env` file in the root directory (see `.env.example` for template) or export your Solar API Key:
```bash
export SOLAR_API_KEY="your_api_key_here"
```

**Note**: Get your API key from [Upstage Platform](https://platform.upstage.ai/)

### 2. Run with Docker (Recommended for DB)
Start the PostgreSQL database:
```bash
docker-compose up -d
```
Access pgAdmin at http://localhost:5050 (log in with admin@admin.com / password).

### 3. Run Backend
```bash
cd backend
pip install -r ../requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
API Docs: http://localhost:8000/docs

### 4. Run Frontend
```bash
cd frontend
streamlit run app.py
```
Access Dashboard: http://localhost:8501

## 🚀 Quick Start

### Run the PoC Demo (Recommended First Step)
```bash
python3 poc_solar_demo.py
```
This demonstrates Solar LLM's effectiveness with real equipment data and shows 100% accuracy results.

### Run Cost Comparison
```bash
python3 llm_comparison.py
python3 cost_calculator.py
```
See why Solar LLM outperforms GPT-4 and Claude 3 for Korean manufacturing use cases.

## Usage
1. Open the Streamlit App.
2. Upload `data/pob_sample.csv`.
3. View the charts.
4. Select an equipment ID and click "Run Solar Analysis".

## 🎯 Why This Matters

This PoC demonstrates:
- **Technical Depth**: Full-stack implementation with ML, LLM, and web technologies
- **Business Acumen**: Complete ROI analysis and go-to-market strategy
- **Solar LLM Expertise**: Deep understanding of Upstage's technology and competitive advantages
- **Market Understanding**: Focus on Korean manufacturing with $5-10B TAM

Perfect for showcasing capabilities in **AI business development** and **enterprise LLM applications**.
