# Speech to Text Project

A professional-grade voice agent application that combines IBM Watson Speech-to-Text (STT) with IBM WatsonX AI to transcribe audio and generate intelligent responses in real-time.

## 🎯 Features

- **Real-time Audio Transcription**: Convert speech to text using IBM Watson Speech-to-Text API
- **AI-Powered Responses**: Process transcriptions with IBM WatsonX LLM (Granite-3-8B)
- **Web Interface**: User-friendly Flask-based web application
- **Multiple Audio Format Support**: Handle various audio formats (WebM, MP3, WAV, etc.)
- **Advanced NLP Features**: Smart formatting, word confidence scores, and timestamps
- **RESTful API**: Seamless integration with frontend applications
- **Production-Ready**: Built with security best practices (environment variables for sensitive data)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         Web Interface (HTML/JS)             │
│              index.html                      │
└────────────────┬────────────────────────────┘
                 │ Audio Stream
                 ▼
┌─────────────────────────────────────────────┐
│      Flask Application Server               │
│            app.py                            │
└────────┬────────────────────────┬───────────┘
         │                        │
         ▼                        ▼
┌──────────────────────┐  ┌──────────────────────┐
│ IBM Watson STT API   │  │ IBM WatsonX API      │
│ watson_stt.py        │  │ watsonx_agent.py     │
└──────────────────────┘  └──────────────────────┘
```

## 📋 Prerequisites

- Python 3.8 or higher
- IBM Cloud account with:
  - Watson Speech-to-Text service
  - WatsonX service with API access
- Required Python packages (see installation)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yaswanthsivala-wq/Speech_to_Text_Project.git
cd Speech_to_Text_Project
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install flask ibm-watson ibm-cloud-sdk-core python-dotenv requests
```

## ⚙️ Configuration

### 1. Create `.env` File
Create a `.env` file in the project root with your IBM Cloud credentials:

```env
# IBM Watson Speech-to-Text
STT_API_KEY=your_stt_api_key_here
STT_URL=https://api.us-south.speech-to-text.watson.cloud.ibm.com

# IBM WatsonX
WATSONX_API_KEY=your_watsonx_api_key_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_PROJECT_ID=your_project_id_here
```

**Note**: The `.env` file is automatically excluded from version control via `.gitignore` for security.

### 2. Obtain IBM Cloud Credentials
- Visit [IBM Cloud Console](https://cloud.ibm.com)
- Create or access your Watson Speech-to-Text and WatsonX services
- Copy API keys and service URLs from the service credentials page

## 🎮 Usage

### Start the Application
```bash
python app.py
```

The application will run on `http://localhost:5000`

### Access the Web Interface
1. Open your browser and navigate to `http://localhost:5000`
2. Use the web interface to record or upload audio
3. View the transcription and AI response in real-time

## 📡 API Endpoints

### `GET /`
Returns the main web interface.

**Response**: HTML page

---

### `POST /transcribe`
Transcribes audio and generates AI response.

**Request**:
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `audio` (file): Audio file to transcribe
  - `mime_type` (string): MIME type of audio (e.g., `audio/webm`, `audio/mp3`)

**Response** (JSON):
```json
{
  "success": true,
  "transcript": "the transcribed text from audio",
  "ai_response": "intelligent response from WatsonX AI"
}
```

**Error Response**:
```json
{
  "error": "error message description"
}
```

## 📁 Project Structure

```
speech-to-text-project/
├── app.py                  # Flask application and routes
├── watson_stt.py           # IBM Watson Speech-to-Text integration
├── watsonx_agent.py        # IBM WatsonX AI integration
├── static/
│   └── script.js           # Frontend JavaScript logic
├── templates/
│   └── index.html          # Web interface
├── .env                    # Environment variables (NOT in GitHub)
├── .gitignore              # Git ignore configuration
└── README.md               # This file
```

## 🔧 Technologies Used

- **Backend**: Flask (Python web framework)
- **Speech-to-Text**: IBM Watson Speech-to-Text API
- **AI/LLM**: IBM WatsonX with Granite-3-8B model
- **Frontend**: HTML5, CSS, JavaScript
- **Authentication**: IBM IAM (Identity and Access Management)
- **Environment Management**: python-dotenv

## 📊 Key Features Explained

### Smart Transcription
- Automatic formatting of dates, times, and numbers
- Word-level confidence scores
- Timestamp information for each word
- Support for multiple audio formats

### AI Response Generation
- Context-aware responses using Granite-3-8B LLM
- Configurable temperature for response creativity (0.7 default)
- Maximum token limit for response length (200 tokens default)
- Real-time processing

## 🛡️ Security

- **Sensitive Data**: API keys and credentials stored in `.env` file (excluded from version control)
- **Input Validation**: Audio file validation before processing
- **Error Handling**: Secure error messages without exposing sensitive information
- **IAM Authentication**: Uses IBM Cloud IAM for secure API communication

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No audio file received" | Ensure audio file is properly attached in the request |
| "API Key error" | Verify `.env` file contains correct credentials from IBM Cloud |
| "Service URL error" | Confirm service URLs match your IBM Cloud region |
| Connection refused | Ensure Flask app is running on port 5000 |

## 📝 License

This project is open-source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📧 Contact

For questions or support, reach out to the project maintainer at `yaswanthsivala-wq` on GitHub.

---

**Last Updated**: April 2026  
**Status**: Production Ready
