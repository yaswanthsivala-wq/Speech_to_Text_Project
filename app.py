from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# 🔑 Replace with your real values
API_KEY = "a-4F4Xn8YjKwohp13bUpqknI3nhN2auGworWn4G2Xw-R"
BASE_URL = "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/2ca270d8-97d1-4a8d-964b-8f132bc9cadc"

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file received'}), 400

    audio_file = request.files['audio']

    # Save incoming file
    temp_path = "recording.webm"
    audio_file.save(temp_path)

    try:
        print("👉 Sending audio to IBM STT...")

        with open(temp_path, 'rb') as f:
            response = requests.post(
                f"{BASE_URL}/v1/recognize",
                headers={
                    "Content-Type": "audio/webm",
                    "Accept": "application/json"
                },
                data=f,
                auth=("apikey", API_KEY),
                timeout=30
            )

        # 🔍 Debug response
        print("👉 IBM RAW RESPONSE:", response.text)

        result = response.json()

        transcript = ""

        if "results" in result and len(result["results"]) > 0:
            transcript = result["results"][0]["alternatives"][0]["transcript"]

        if transcript.strip() == "":
            transcript = "⚠️ Could not recognize speech"

        return jsonify({
            "success": True,
            "transcript": transcript
        })

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == '__main__':
    app.run(debug=True)