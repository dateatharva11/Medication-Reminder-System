# Medication Reminder System

## Overview
The **Medication Reminder System** is a Flask-based application that leverages Twilio, ElevenLabs, and Deepgram to send automated voice reminders to patients about their medications. The system makes calls, records responses, and logs patient interactions.

## Features
- **Automated Calls**: Initiates a call to the patient with a medication reminder.
- **Voice Prompts & TTS**: Uses Twilio and ElevenLabs for text-to-speech conversion.
- **Response Recording & STT**: Captures patient responses and transcribes them using Deepgram.
- **Unanswered Call Handling**: Sends an SMS if the patient doesn't pick up.
- **Patient-Initiated Calls**: Allows patients to call back and hear the reminder again.
- **Web Interface**: Simple frontend for initiating calls via a web form.

## Project Structure
```
/medication-reminder
│── /static
│   ├── styles.css        # Styling for the web UI
│   ├── script.js         # JavaScript for handling call requests
│── /templates
│   ├── index.html        # Web interface
│── app.py                # Main Flask application
│── .env                  # Environment variables
│── requirements.txt      # Dependencies
│── README.md             # Documentation
```

## Installation & Setup

### Clone the Repository
```sh
git clone https://github.com/dateatharva11/Medication-Reminder-System.git
cd Medication-Reminder-System
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Set Up Environment Variables
Add your API keys for **Twilio, Deepgram, and ElevenLabs** to the `.env` file.

### Run the Flask App
```sh
python app.py
```
The server should start at: `http://127.0.0.1:5000/`

## Using LocalTunnel for Public API Access

### Install LocalTunnel
```sh
npm install -g localtunnel
```

### Start LocalTunnel
```sh
lt --port 5000
```

### Update Twilio Webhook URLs
Edit `app.py` and replace:
```python
url = "https://your-localtunnel-url.loca.lt/voice_prompt"
```

## How the System Works

### Outgoing Call Flow
1. The `/call` endpoint is triggered via Postman or the web interface.
2. Twilio makes a call to `PATIENT_PHONE_NUMBER`.
3. The patient hears a medication reminder and is prompted to respond.
4. If the patient speaks, the response is recorded and logged.

### Patient Response Handling
1. If the patient responds, the `/process_response` endpoint logs it.
2. The system thanks the patient for their response.

### Handling Unanswered Calls
1. If the patient doesn't pick up, Twilio redirects to `/unanswered`.
2. A voicemail is left, and an SMS reminder is sent.

### Patient-Initiated Call
1. If the patient calls back, `/incoming_call` plays the reminder again.

## Testing the System Using Web Interface
1. Open `http://127.0.0.1:5000/templates/index.html` in a browser.
2. Enter the patient's phone number.
3. Click **"Send Reminder"**.
4. The system will initiate a call and display the status.

---
### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Author
Developed by **Atharva Shailesh Date**

### Contact
For issues or suggestions, please open an issue in the repository.
