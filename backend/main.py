from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import pandas as pd
import io
from datetime import datetime
from typing import List
from dotenv import load_dotenv
import os

# Load env vars from parent directory (where .env usually is in this structure)
# or current directory if running from backend
load_dotenv() 
# Also try loading from parent dir if not found (development convenience)
load_dotenv("../.env")

import sys
sys.path.insert(0, '/Users/curi/Desktop/PoC/askup-poc')

from backend.database import SessionLocal, engine
from backend import models
from backend.xgboost_model import predictor
from backend.solar_client import analyze_failure

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AskUp PoC API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    # Preprocessing & Inference
    results = []
    
    for _, row in df.iterrows():
        # Predict failure if not in CSV (assuming CSV might just have sensor data)
        # But user says CSV has labels? "전처리: 결측치 처리, 한국어 고장 유형 라벨링"
        # Let's assume we just store and maybe re-predict or use the label if present.
        # Requirement says: "POST /upload_csv → PostgreSQL 저장"
        # We will also run the XGBoost predictor to verify or fill gaps?
        # Let's trust the CSV data but also allow prediction if needed.
        
        # Simple prediction check
        pred_failure = predictor.predict(row['temp'], row['vibration'], row['pressure'])
        
        # If 'failure_type' is in CSV, use it, else use prediction ?? 
        # Requirement: "simple XGBoost failure prediction model training"
        # Let's just store what we have.
        
        failure_val = row.get('failure_type', pred_failure)
        
        db_log = models.VocLog(
            timestamp=pd.to_datetime(row['timestamp']),
            equipment_id=row['equipment_id'],
            temp=row['temp'],
            vibration=row['vibration'],
            pressure=row['pressure'],
            failure_type=int(failure_val)
        )
        db.add(db_log)
        results.append(db_log)
    
    db.commit()
    return {"message": f"Successfully processed {len(results)} rows"}

@app.post("/analyze/{equipment_id}")
def analyze_equipment(equipment_id: str, db: Session = Depends(get_db)):
    # Get latest log for this equipment
    log = db.query(models.VocLog).filter(models.VocLog.equipment_id == equipment_id).order_by(models.VocLog.timestamp.desc()).first()
    
    if not log:
        raise HTTPException(status_code=404, detail="Equipment not found")
        
    # Call Solar LLM
    analysis = analyze_failure(equipment_id, log.temp, log.vibration, log.pressure)
    
    # Save analysis to DB
    log.solar_analysis = analysis
    db.commit()
    
    return analysis

@app.get("/dashboard_data")
def get_dashboard_data(db: Session = Depends(get_db)):
    # Aggregates for charts
    logs = db.query(models.VocLog).all()
    if not logs:
        return {"data": []}
        
    data = []
    for log in logs:
        data.append({
            "timestamp": log.timestamp,
            "equipment_id": log.equipment_id,
            "temp": log.temp,
            "vibration": log.vibration,
            "pressure": log.pressure,
            "failure_type": log.failure_type,
            "analysis": log.solar_analysis
        })
    return {"data": data}
