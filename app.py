import os
from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from elevenlabs import generate, set_api_key
from deepgram import Deepgram
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load API keys and Twilio credentials
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
PATIENT_PHONE_NUMBER = os.getenv("PATIENT_PHONE_NUMBER")

# Setting up keys 
set_api_key(ELEVENLABS_API_KEY)
deepgram = Deepgram(DEEPGRAM_API_KEY)
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Text to Speech Function
def text_to_speech(text, voice="Aria"):
    """Convert text to speech using ElevenLabs API."""
    audio = generate(
        text=text,
        voice=voice,
        model="eleven_multilingual_v2"
    )
    return audio

# Speech to Text Function
def speech_to_text(audio_file_path):
    """Convert speech to text using Deepgram API."""
    with open(audio_file_path, 'rb') as audio_file:
        audio_content = audio_file.read()
    
    source = {'buffer': audio_content, 'mimetype': 'audio/wav'}
    options = {'punctuate': True, 'language': 'en-US', 'model': 'general'}

    response = deepgram.transcription.sync_prerecorded(source, options)
    
    return response['results']['channels'][0]['alternatives'][0]['transcript']

@app.route('/')
def home():
    return "Welcome to the Medication Reminder System API. Use /call to trigger a reminder."

# Outgoing Call to Patient
@app.route('/call', methods=['POST'])
def make_call():
    """Initiate an outgoing call with medication reminder using Twilio."""
    call = twilio_client.calls.create(
        to=PATIENT_PHONE_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        url="https://your-localtunnel-url.loca.lt/voice_prompt"
    )
    print(f"Call initiated: SID {call.sid}, Status: Initiated")
    return jsonify({"message": "Call initiated", "call_sid": call.sid}), 200

# Twilio Voice Prompt for Medication Confirmation
@app.route('/voice_prompt', methods=['POST'])
def voice_prompt():
    """Twilio calls this URL to provide medication reminder via TTS."""
    response = VoiceResponse()
    response.say("Hello, this is a reminder from your healthcare provider. "
                 "Please confirm if you have taken your prescribed medications today. "
                 "Say 'Yes' if you have taken your medications or 'No' if you haven't.",
                 voice="alice", language="en-US")
    response.record(timeout=5, transcribe=True, action="/process_response")
    return str(response)

# Process Patient Response
@app.route('/process_response', methods=['POST'])
def process_response():
    """Capture and log the patient's response."""
    recording_url = request.form.get("RecordingUrl", "")
    transcript = ""
    
    if recording_url:
        print(f"Recording URL: {recording_url}")
        # Fetching the transcription of the recorded message
        transcript = request.form.get("TranscriptionText", "")
        print(f"Patient Response Recorded: {transcript}")
    
    # Log call data to console
    call_sid = request.form.get("CallSid", "")
    call_status = request.form.get("CallStatus", "Unknown")
    print(f"Call SID: {call_sid}, Status: {call_status}, Response: {transcript}")

    response = VoiceResponse()
    response.say("Thank you for your response. Have a great day!", voice="alice")
    return str(response)

# Handle Unanswered Calls & Voicemail
@app.route('/unanswered', methods=['POST'])
def unanswered_call():
    """Leave a voicemail or send SMS if the patient doesn't answer."""
    response = VoiceResponse()
    response.say("We called to check on your medication but couldn't reach you. "
                 "Please call us back or take your medications if you haven't done so.", voice="alice")
    
    # Send SMS if voicemail is unavailable
    twilio_client.messages.create(
        body="We couldn't reach you for your medication confirmation. Please call us back or take your medications.",
        from_=TWILIO_PHONE_NUMBER,
        to=PATIENT_PHONE_NUMBER
    )

    # Log call data to console
    print(f"Call SID: Unanswered, Status: Voicemail left, Response: Voicemail left. SMS sent.")

    return str(response)

# Handle Patient-Initiated Calls
@app.route('/incoming_call', methods=['POST'])
def incoming_call():
    """Replay medication reminder when patient calls back."""
    response = VoiceResponse()
    response.say("Hello, this is a reminder from your healthcare provider. "
                 "Please confirm if you have taken your medications today.",
                 voice="alice", language="en-US")
    response.record(timeout=5, transcribe=True, action="/process_response")
    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
