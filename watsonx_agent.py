import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_iam_token():
    response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": os.getenv('WATSONX_API_KEY')
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return response.json()["access_token"]


def process_with_watsonx(transcript):
    token = get_iam_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
    "model_id": "ibm/granite-3-8b-instruct",
        "project_id": os.getenv('WATSONX_PROJECT_ID'),
        "input": f"User said: {transcript}. Respond clearly.",
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7
        }
    }

    response = requests.post(
        f"{os.getenv('WATSONX_URL')}/ml/v1/text/generation?version=2023-05-29",
        json=payload,
        headers=headers
    )

    if response.status_code != 200:
        return f"Error: {response.text}"

    return response.json()['results'][0]['generated_text']