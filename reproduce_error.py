import requests
import pandas as pd
from io import BytesIO

url = "http://127.0.0.1:8000/predict_batch"

# Create a sample CSV
data = {
    'intern_id': ['INT-001', 'INT-002'],
    'task_completion_rate': [0.8, 0.9],
    'consistency_score': [0.7, 0.85],
    'engagement_metric': [0.6, 0.8]
}
df = pd.DataFrame(data)
csv_buffer = BytesIO()
df.to_csv(csv_buffer, index=False)
csv_buffer.seek(0)

print("Testing CSV upload...")
try:
    files = {'file': ('test.csv', csv_buffer, 'text/csv')}
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Create a sample Excel
excel_buffer = BytesIO()
df.to_excel(excel_buffer, index=False)
excel_buffer.seek(0)

print("\nTesting Excel upload...")
try:
    files = {'file': ('test.xlsx', excel_buffer, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
