from flask import Flask, request, jsonify, render_template
import os
import tempfile
import uuid
import json

from watson_stt import transcribe_audio
from watsonx_agent import process_with_watsonx

app = Flask(__name__)

conversation_history = []


@app.route('/')
def home():
    return render_template('index.html')


# 🎤 MIC TRANSCRIBE (MULTILINGUAL + CLASSIFICATION)
@app.route('/transcribe', methods=['POST'])
def transcribe():

    if 'audio' not in request.files:
        return jsonify({'error': 'No audio received'}), 400

    audio_file = request.files['audio']

    temp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.webm")
    audio_file.save(temp_path)

    try:
        print("👉 Transcribing...")

        # 🎤 Speech to Text
        transcript = transcribe_audio(temp_path, "audio/webm")

        if transcript.strip() == "":
            transcript = "⚠️ Could not recognize speech"

        print("📝 USER:", transcript)

        # 🧠 MULTI LANGUAGE + CLASSIFICATION PROMPT
        prompt = f"""
You are an AI insurance assistant.

The user may speak in ANY language (English, Telugu, Hindi, Spanish, etc).
Understand the meaning correctly.

From the conversation below:

1. Detect the language
2. Understand intent
3. Convert to English if needed
4. Return STRICT JSON only:

{{
  "summary": "short summary in English",
  "type": "Auto | Health | Life | Property"
}}

Conversation:
{transcript}
"""

        ai_response = process_with_watsonx(prompt)

        print("🤖 RAW AI:", ai_response)

        # 🔥 PARSE JSON SAFELY
        try:
            parsed = json.loads(ai_response)
            summary = parsed.get("summary", "")
            insurance_type = parsed.get("type", "Other")
        except:
            summary = ai_response
            insurance_type = "Other"

        print("📊 SUMMARY:", summary)
        print("🏷️ TYPE:", insurance_type)

        return jsonify({
            "transcript": transcript,
            "summary": summary,
            "type": insurance_type
        })

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception as e:
            print("⚠️ File delete issue:", e)


# 📁 FILE UPLOAD (SAME LOGIC)
@app.route('/upload', methods=['POST'])
def upload():

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    temp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.wav")
    file.save(temp_path)

    try:
        transcript = transcribe_audio(temp_path, "audio/wav")

        prompt = f"""
You are an AI insurance assistant.

Analyze this conversation and return STRICT JSON:

{{
  "summary": "short summary",
  "type": "Auto | Health | Life | Property"
}}

Conversation:
{transcript}
"""

        ai_response = process_with_watsonx(prompt)

        try:
            parsed = json.loads(ai_response)
            summary = parsed.get("summary", "")
            insurance_type = parsed.get("type", "Other")
        except:
            summary = ai_response
            insurance_type = "Other"

        return jsonify({
            "transcript": transcript,
            "summary": summary,
            "type": insurance_type
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except:
            pass


if __name__ == '__main__':
    app.run(debug=True)