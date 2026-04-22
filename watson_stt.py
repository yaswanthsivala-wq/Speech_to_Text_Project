from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
from dotenv import load_dotenv

load_dotenv()

def transcribe_audio(audio_file_path, mime_type):
    authenticator = IAMAuthenticator(os.getenv('STT_API_KEY'))
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(os.getenv('STT_URL'))

    with open(audio_file_path, 'rb') as audio_file:
        result = speech_to_text.recognize(
            audio=audio_file,
            content_type=mime_type,
            model='en-US_BroadbandModel',
            smart_formatting=True,
            word_confidence=False,   # 🔥 not needed → faster
            timestamps=False         # 🔥 not needed → faster
        ).get_result()

    transcript = ""

    for chunk in result.get('results', []):
        transcript += chunk['alternatives'][0]['transcript'] + " "

    # 🔥 CLEAN TEXT
    transcript = transcript.replace("%HESITATION", "")
    transcript = transcript.strip()

    return transcript