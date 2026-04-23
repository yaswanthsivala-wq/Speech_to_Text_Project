import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")


# 🔐 GET IAM TOKEN (SAFE VERSION)
def get_iam_token():
    url = "https://iam.cloud.ibm.com/identity/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}"

    response = requests.post(url, headers=headers, data=data)
    result = response.json()

    print("👉 IAM RESPONSE:", result)

    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"IAM token error: {result}")


# 🤖 WATSONX PROCESS
def process_with_watsonx(context):
    try:
        token = get_iam_token()

        url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        body = {
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": context}
            ],
            "model_id": "ibm/granite-4-h-small",
            "project_id": PROJECT_ID
        }

        response = requests.post(url, headers=headers, json=body)

        print("STATUS:", response.status_code)
        print("FULL RESPONSE:", response.text)

        result = response.json()

        # ✅ Handle Chat response
        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        # ✅ Handle fallback (older format)
        elif "results" in result:
            return result["results"][0]["generated_text"]

        else:
            return "⚠️ AI did not return valid response"

    except Exception as e:
        print("❌ WatsonX ERROR:", str(e))
        return "⚠️ AI processing error"