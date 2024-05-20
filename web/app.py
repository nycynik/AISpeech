from io import BytesIO

from openai import OpenAI
from flask import Flask, render_template, send_file, request
import logging

client = OpenAI()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/listen")
def listen():
     return render_template("stt.html")

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    try:
        if not "file" in request.files:
             return "missing audio file", 400
         
        file = request.files["file"]
        handle = BytesIO(file.read())
        handle.name = file.filename
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=handle, 
            response_format="text",
        )
    
        return transcript
    
    except Exception as e:
            logging.error(f"An error occurred during transcribe processing: {e}")
            return "An error occurred while processing the request", 500

@app.route("/tts", methods=["POST"])
def tts():
    try:
        data = request.get_json()
        
        text = data.get("text", "")
        if text is None:
            return "Text is missing and required", 400
        
        voice = data.get("voice", "alloy")

        response = client.audio.speech.create(
            model="tts-1",
            voice=voice, 
            input=text,
        )

        return send_file(BytesIO(response.read()), mimetype="audio/mp3")
    
    except Exception as e:
            logging.error(f"An error occurred during TTS processing: {e}")
            return "An error occurred while processing the request", 500

# and let's go!
# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# Create a file handler and set its level to error
log_handler = logging.FileHandler('error.log')
log_handler.setLevel(logging.ERROR)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(log_handler)

# Run the app
app.run(debug=True)