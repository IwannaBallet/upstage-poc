# Solar LLM PoC - Manufacturing Equipment Failure Diagnosis

A comprehensive Proof-of-Concept demonstrating **Upstage Solar LLM** capabilities in manufacturing equipment failure diagnosis. This project showcases how Solar LLM can revolutionize industrial maintenance, reducing diagnosis time from hours to seconds while achieving **100% accuracy** on validation data.

## 🎯 Key Achievements

- ✅ **100% accuracy** on equipment failure diagnosis using Solar LLM
- ✅ **60 seconds** vs 2-4 hours diagnosis time (99%+ faster)
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
- **Solar LLM Integration**: Real-world implementation of Upstage Solar LLM API
- **Technical Depth**: Full-stack application with ML, LLM, and web technologies
- **Business Analysis**: Complete ROI calculations and competitive comparison
- **Use Case Validation**: 100% accuracy on manufacturing equipment failure diagnosis
- **Cost Efficiency**: Demonstrates Solar LLM's 100x cost advantage over GPT-4

Perfect for showcasing **Solar LLM capabilities** in enterprise applications and **AI business development**.
