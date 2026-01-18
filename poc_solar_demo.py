#!/usr/bin/env python3
"""
AskUp PoC - Solar LLM API Evaluation
======================================
This script demonstrates the Solar LLM API's capability to analyze
industrial equipment sensor data and provide failure diagnostics.
"""

import os
import sys
import json
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
load_dotenv("../.env")

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from backend.solar_client import analyze_failure

def load_sample_data():
    """Load sample data from CSV"""
    csv_path = Path(__file__).parent / "data" / "pob_sample.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)
    else:
        # Create sample data if not found
        print("Sample CSV not found, using hardcoded data...")
        data = {
            'timestamp': [
                '2023-10-27 10:00:00', '2023-10-27 10:05:00',
                '2023-10-27 10:10:00', '2023-10-27 10:15:00',
                '2023-10-27 10:20:00'
            ],
            'equipment_id': ['EQ-101', 'EQ-101', 'EQ-102', 'EQ-103', 'EQ-102'],
            'temp': [65.5, 68.2, 95.1, 64.0, 98.4],
            'vibration': [12.1, 14.5, 45.2, 11.0, 48.9],
            'pressure': [101.2, 100.8, 90.5, 101.5, 88.2],
            'failure_type': [0, 0, 1, 0, 1]
        }
        return pd.DataFrame(data)

def print_header():
    """Print PoC header"""
    print("\n" + "="*70)
    print("🏭 AskUp PoC - Solar LLM API Evaluation")
    print("="*70)
    print("Purpose: Test if Solar LLM API is suitable for equipment failure diagnosis")
    print("="*70 + "\n")

def print_results(equipment_id, temp, vibration, pressure, failure_type, analysis):
    """Print formatted results"""
    print(f"\n{'─'*70}")
    print(f"Equipment: {equipment_id}")
    print(f"{'─'*70}")
    print(f"Sensor Data:")
    print(f"  • Temperature: {temp}°C")
    print(f"  • Vibration: {vibration} Hz")
    print(f"  • Pressure: {pressure} Pa")
    print(f"  • Actual Status: {'⚠️  FAILURE' if failure_type == 1 else '✅ NORMAL'}")
    print(f"\n{'─'*70}")
    print("Solar LLM Analysis:")
    print(f"{'─'*70}")
    
    if isinstance(analysis, dict) and "error" in analysis:
        print(f"❌ Error: {analysis['error']}")
        print(f"   {analysis.get('analysis', 'No API response')}")
    else:
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
    
    print()

def main():
    print_header()
    
    # Check API key
    api_key = os.getenv("SOLAR_API_KEY")
    if not api_key:
        print("⚠️  WARNING: SOLAR_API_KEY environment variable not set")
        print("   To use Solar LLM API, set: export SOLAR_API_KEY='your-key-here'")
        print("   Get your API key from: https://www.upstage.ai/\n")
    
    # Load sample data
    print("📊 Loading sample data...")
    df = load_sample_data()
    print(f"✅ Loaded {len(df)} equipment records\n")
    
    # Analyze each record
    print("🔍 Running Solar LLM Analysis on sample data...\n")
    
    results_summary = {
        'total_analyzed': len(df),
        'normal_correct': 0,
        'failure_correct': 0,
        'errors': 0
    }
    
    for idx, row in df.iterrows():
        equipment_id = row['equipment_id']
        temp = row['temp']
        vibration = row['vibration']
        pressure = row['pressure']
        failure_type = row['failure_type']
        
        # Call Solar LLM API
        analysis = analyze_failure(equipment_id, temp, vibration, pressure)
        
        # Print results
        print_results(equipment_id, temp, vibration, pressure, failure_type, analysis)
        
        # Track results
        if isinstance(analysis, dict):
            if "error" in analysis:
                results_summary['errors'] += 1
            else:
                # Try to extract status from analysis
                status = analysis.get('status', '').lower() if isinstance(analysis, dict) else str(analysis).lower()
                
                if failure_type == 0 and '정상' in status:
                    results_summary['normal_correct'] += 1
                elif failure_type == 1 and ('주의' in status or '위협' in status or '고장' in status):
                    results_summary['failure_correct'] += 1
    
    # Print summary
    print("\n" + "="*70)
    print("📈 Analysis Summary")
    print("="*70)
    print(f"Total Records Analyzed: {results_summary['total_analyzed']}")
    print(f"Normal Status Correctly Identified: {results_summary['normal_correct']}")
    print(f"Failure Status Correctly Identified: {results_summary['failure_correct']}")
    print(f"API Errors: {results_summary['errors']}")
    
    if results_summary['errors'] == 0 and results_summary['total_analyzed'] > 0:
        accuracy = ((results_summary['normal_correct'] + results_summary['failure_correct']) / 
                   results_summary['total_analyzed']) * 100
        print(f"\n✅ Overall Accuracy: {accuracy:.1f}%")
    
    print("\n" + "="*70)
    print("💡 Verdict: Is Solar LLM API Worth It?")
    print("="*70)
    if results_summary['errors'] == 0:
        if accuracy >= 80:
            print("✅ RECOMMENDED - Solar LLM provides reliable failure diagnosis")
        else:
            print("⚠️  NEEDS TUNING - API works but accuracy needs improvement")
    else:
        print("❌ NOT RECOMMENDED - API has connectivity or format issues")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
