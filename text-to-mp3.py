#RUSSELLS SCRIPT.  Change the below variables and then request a new mp3 file. avoid using tts on stuff she says over and over.


#to run:

#cd /path/to/folder
#python3 text-to-mp3.py

#the text to turn into an mp3
text = "I'll call you"

#the output file name (must be six or more characters. too short a name and it doesnt get written for some reason)

output_file="new-op.mp3"

# Used for Google Cloud Text-to-Speech functionality
from google.cloud import texttospeech

# Used for file and folder operations
import os

#Initialize the text to speech, speech to text, maps credential json file.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-creds.json"

def text_to_speech():
    print(text)
    print(output_file)
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", name="en-US-Wavenet-F"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # Save the synthesized audio to a file
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content attempted written to file "{output_file}"')

def main():
    text_to_speech()

main()
