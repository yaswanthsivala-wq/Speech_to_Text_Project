from dotenv import load_dotenv
load_dotenv()
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

api_key = os.getenv("STT_API_KEY")
url = os.getenv("STT_URL")

authenticator = IAMAuthenticator(api_key)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(url)


def transcribe_audio(file_path, content_type):

    with open(file_path, "rb") as audio_file:

        response = stt.recognize(
            audio=audio_file,
            content_type=content_type,
            model="en-US_Multimedia",   # 🔥 BEST MODEL
            smart_formatting=True,
            timestamps=False,
            word_confidence=False
        ).get_result()

    text = ""

    for res in response['results']:
        text += res['alternatives'][0]['transcript']

    return text.strip()