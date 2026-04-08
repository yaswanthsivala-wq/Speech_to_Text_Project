from flask import Flask, request, jsonify, render_template
from watson_stt import transcribe_audio
from watsonx_agent import process_with_watsonx
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file received'}), 400

    audio_file = request.files['audio']

    # Get correct file extension
    original_filename = audio_file.filename or 'recording.webm'
    extension = original_filename.rsplit('.', 1)[-1]
    temp_path = f'temp_recording.{extension}'

    audio_file.save(temp_path)

    # ✅ IMPORTANT: get mime type from frontend
    mime_type = request.form.get('mime_type', 'audio/webm')

    try:
        transcript = transcribe_audio(temp_path, mime_type)
        ai_response = process_with_watsonx(transcript)

        return jsonify({
            'success': True,
            'transcript': transcript,
            'ai_response': ai_response
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == '__main__':
    print("Running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)