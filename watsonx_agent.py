import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# 🔥 STEP 1 — GET IAM TOKEN
def get_iam_token():
    url = "https://iam.cloud.ibm.com/identity/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}"

    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]


# 🔥 STEP 2 — CALL WATSONX
def process_with_watsonx(context):
    try:
        token = get_iam_token()

        url = url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        body = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                    },
                {
                    "role": "user",
                    "content": context
                    }
                ],
            "max_tokens": 200,
            "model_id": "ibm/granite-4-h-small",
            "project_id": PROJECT_ID
}

        response = requests.post(url, headers=headers, json=body)

        result = response.json()
        print("👉 Watsonx RAW RESPONSE:", result)
        
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        
        return "⚠️ AI did not return valid response"


    except Exception as e:
        print("❌ Watsonx ERROR:", str(e))
        return "⚠️ AI processing error"