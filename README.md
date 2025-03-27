Medication Reminder System - Documentation


Overview
The Medication Reminder System is a Flask-based application that leverages Twilio, ElevenLabs, and Deepgram to send automated voice reminders to patients about their medications. The system makes calls, records responses, and logs patient interactions.


Features
- Automated Calls: Initiates a call to the patient with a medication reminder.
- Voice Prompts & TTS: Uses Twilio and ElevenLabs for text-to-speech conversion.
- Response Recording & STT: Captures patient responses and transcribes them using Deepgram.
- Unanswered Call Handling: Sends an SMS if the patient doesn't pick up.
- Patient-Initiated Calls: Allows patients to call back and hear the reminder again.
- Web Interface: Simple frontend for initiating calls via a web form.


Project Structure

/medication-reminder
│── /static
│   ├── styles.css    # Styling for the web UI
│   ├── script.js     # JavaScript for handling call requests
│── templates/
│   ├── index.html    # Web interface
│── app.py            # Main Flask application
│── .env              # Environment variables
│── requirements.txt  # Dependencies
│── README.md         # Documentation


Installation & Setup

1. Clone the Repository
git clone https://github.com/dateatharva11/Medication-Reminder-System.git
cd Medication-Reminder-System

2. Install Dependencies
pip install -r requirements.txt

3. Set Up Environment Variables
Add your API keys for Twilio, Deepgram and ElevenLabs to the .env file

4. Run the Flask App
The server should start at http://127.0.0.1:5000/
python app.py

5. Using LocalTunnel for Public API Access
1) Install LocalTunnel 
npm install -g localtunnel

2) Start LocalTunnel
lt --port 5000

3) Update Twilio Webhook URLs
Edit app.py and replace:
url="https://your-localtunnel-url.loca.lt/voice_prompt"


How the System Works
1) Outgoing Call Flow
- The /call endpoint is triggered via Postman or the web interface.
- Twilio makes a call to PATIENT_PHONE_NUMBER.
- The patient hears a medication reminder and is prompted to respond.
- If the patient speaks, the response is recorded and logged.

2) Patient Response Handling
- If the patient responds, the /process_response endpoint logs it.
- The system thanks the patient for their response.

3) Handling Unanswered Calls
- If the patient doesn't pick up, Twilio redirects to /unanswered.
- A voicemail is left, and an SMS reminder is sent.

4) Patient-Initiated Call
- If the patient calls back, /incoming_call plays the reminder again.


Testing the system using Web Interface:

- Open http://127.0.0.1:5000/templates/index.html in a browser.
- Enter the patient's phone number.
- Click "Send Reminder".
- The system will initiate a call and display the status.

