from pathlib import Path
from openai import OpenAI
client = OpenAI()

speech_file_path = Path(__file__).parent / "../output/doorajar.mp3"
input_text = "The door is open."

response = client.audio.speech.create(
  model="tts-1",
  voice="nova",
  input=input_text
)

response.stream_to_file(speech_file_path)

print ("MP3 Created!")
