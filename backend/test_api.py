from fastapi.testclient import TestClient
import json
import main

client = TestClient(main.app)

payload = {
    "symptoms": "Itchy rash on groin area for 3 months, intermittent redness and scaling.",
    "age": 54,
    "gender": "male",
    "duration": "3 months",
    "severity": 5
}

resp = client.post('/api/diagnose', json=payload)
print('Status code:', resp.status_code)
try:
    data = resp.json()
    print('Keys:', list(data.keys()))
    answer = data.get('answer', '')
    print('\n--- Answer (first 800 chars) ---\n')
    print(answer[:800])
except Exception as e:
    print('Failed to parse JSON response:', e)
    print('Raw response text:\n', resp.text)
