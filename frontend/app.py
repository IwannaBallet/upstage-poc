import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import json
import io

# Setup
st.set_page_config(page_title="Solar LLM Factory Monitor", layout="wide")
API_URL = "http://localhost:8000"

st.title("🏭 Solar LLM Smart Factory Dashboard")

# Sidebar
st.sidebar.header("Control Panel")

# 1. CSV Upload
uploaded_file = st.sidebar.file_uploader("Upload Sensor Log (CSV)", type="csv")

if uploaded_file is not None:
    if st.sidebar.button("Process & Upload"):
        files = {"file": uploaded_file.getvalue()}
        try:
            res = requests.post(f"{API_URL}/upload_csv", files={"file": uploaded_file})
            if res.status_code == 200:
                st.sidebar.success("Upload Successful!")
            else:
                st.sidebar.error(f"Error: {res.text}")
        except Exception as e:
            st.sidebar.error(f"Connection Error: {e}")

# Main Dashboard
try:
    res = requests.get(f"{API_URL}/dashboard_data")
    data = res.json().get("data", [])
    
    if data:
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Top Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Logs", len(df))
        fail_count = df[df['failure_type'] == 1].shape[0]
        col2.metric("Failure Instances", fail_count)
        avg_temp = df['temp'].mean()
        col3.metric("Avg Temperature", f"{avg_temp:.1f}°C")
        
        # Charts
        st.subheader("Sensor Trends")
        fig_temp = px.line(df, x='timestamp', y='temp', color='equipment_id', title="Temperature Over Time")
        st.plotly_chart(fig_temp, use_container_width=True)
        
        fig_vib = px.bar(df, x='equipment_id', y='vibration', color='failure_type', title="Vibration Levels by Equipment")
        st.plotly_chart(fig_vib, use_container_width=True)
        
        # LLM Analysis Section
        st.subheader("🤖 AI Diagnostic Assistant")
        
        eq_list = df['equipment_id'].unique()
        selected_eq = st.selectbox("Select Equipment to Analyze", eq_list)
        
        if st.button("Run Solar Analysis"):
            with st.spinner("Asking Solar LLM..."):
                try:
                    res_an = requests.post(f"{API_URL}/analyze/{selected_eq}")
                    if res_an.status_code == 200:
                        analysis_result = res_an.json()
                        st.json(analysis_result)
                        
                        # Display nicely
                        if "diagnosis" in analysis_result:
                            st.success(f"Diagnosis: {analysis_result['diagnosis']}")
                            st.info(f"Recommendation: {analysis_result['recommendation']}")
                        else:
                            st.write(analysis_result)
                            
                except Exception as e:
                    st.error(f"Analysis failed: {e}")

    else:
        st.info("No data available. Please upload a CSV.")

except Exception as e:
    st.error(f"Could not connect to backend. Is it running? {e}")
