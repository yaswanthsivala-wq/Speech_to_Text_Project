from flask import Flask, request, jsonify, render_template
import os

from watson_stt import transcribe_audio
from watsonx_agent import process_with_watsonx

app = Flask(__name__)

# 🧠 MEMORY
conversation_history = []

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file received'}), 400

    audio_file = request.files['audio']

    temp_path = "recording.webm"
    audio_file.save(temp_path)

    try:
        print("👉 Transcribing using IBM SDK...")

        transcript = transcribe_audio(temp_path, "audio/webm")
        transcript = transcript.replace("%HESITATION", "").strip()

        if transcript == "":
            transcript = "⚠️ Could not recognize speech"

        print("📝 USER:", transcript)

        # 🧠 ADD USER INPUT
        conversation_history.append(f"User: {transcript}")

        # 🔥 CONTEXT
        context = "\n".join(conversation_history[-5:])

        # 🤖 AI
        ai_response = process_with_watsonx(context)
        ai_response = ai_response.replace("Assistant:", "").strip()

        print("🤖 AI:", ai_response)

        # 🧠 SAVE AI RESPONSE
        conversation_history.append(f"Assistant: {ai_response}")

        return jsonify({
            "success": True,
            "transcript": transcript,
            "ai_response": ai_response
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


if __name__ == '__main__':
    app.run(debug=True)