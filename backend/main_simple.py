from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from datetime import datetime
from typing import List

app = FastAPI(title="Solar LLM PoC API")

# Add CORS support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database
data_storage = []

@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    """Upload and process CSV file"""
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Store the data
        for _, row in df.iterrows():
            record = {
                "timestamp": row.get('timestamp', datetime.now().isoformat()),
                "equipment_id": row.get('equipment_id', 'unknown'),
                "temp": float(row.get('temp', 0)),
                "vibration": float(row.get('vibration', 0)),
                "pressure": float(row.get('pressure', 0)),
                "failure_type": int(row.get('failure_type', 0))
            }
            data_storage.append(record)
        
        return {
            "message": f"Successfully processed {len(df)} rows",
            "rows_processed": len(df)
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to process CSV"
        }

@app.get("/dashboard_data")
def get_dashboard_data():
    """Get dashboard data"""
    if not data_storage:
        return {"data": []}
    
    return {"data": data_storage}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "total_records": len(data_storage)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
