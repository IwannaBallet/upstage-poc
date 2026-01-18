import os
import requests
import json

SOLAR_API_KEY = os.getenv("SOLAR_API_KEY")
SOLAR_API_URL = "https://api.upstage.ai/v1/solar/chat/completions"

def analyze_failure(equipment_id, temp, vibration, pressure):
    if not SOLAR_API_KEY:
        return {
            "error": "SOLAR_API_KEY not found",
            "analysis": "API Key missing. Cannot perform LLM analysis."
        }

    prompt = f"""
    당신은 제조 설비 전문가입니다. 다음 센서 데이터를 바탕으로 장비의 상태를 분석하고 고장 유형과 원인을 추론해주세요.
    
    장비 ID: {equipment_id}
    온도: {temp}도
    진동: {vibration}Hz
    압력: {pressure}Pa
    
    분석 결과는 다음 JSON 형식으로 출력해주세요:
    {{
        "status": "정상" 또는 "주의" 또는 "위협",
        "diagnosis": "고장 원인 분석 내용 (한글)",
        "recommendation": "조치 사항 (한글)"
    }}
    """
    
    headers = {
        "Authorization": f"Bearer {SOLAR_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "solar-1-mini-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful industrial maintenance assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }
    
    try:
        response = requests.post(SOLAR_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Try to parse JSON from content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback if LLM doesn't return pure JSON
            return {"raw_analysis": content}
            
    except Exception as e:
        return {"error": str(e)}
