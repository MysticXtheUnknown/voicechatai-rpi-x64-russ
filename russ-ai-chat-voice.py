#version 1.0 Z
#check licenses folder for software licenses.

#the decibals can be seen in the output when blueberry has been activated, please use a decibal level that provides maximum functionality.  This is used by the silence detector, when silence is detected for two seconds (below threshold), the speech input ends.

my_threshold = -37  #edutige eim 003

#my_threshold = -40 #my headphones with inline mic.

my_name = "no name" #default value, gets written over as the name loads from my-name-is.txt

about_me = "nothing" #populated by the about-me.txt

#This next line is fed to the ai when chat_history.txt gets deleted and you start a new history. the ai wont remember it forever because the chat_history gets truncated when it gets long.

# Used to work with sockets, for example, to get the hostname
import socket

# Used for file and folder operations
import os

# Used to run a shell command, for example, to set the background image
import subprocess

# Used to get the current user's username
import getpass

# Used for making HTTP requests, for example, to generate images and get weather information
import requests

# Used for working with JSON data, for example, when processing API responses
import json

# Used for making URL requests, for example, to download an image
import urllib.request

# Used to calculate the time difference between two network speed measurements
import time

# Used to work with the Pygame library for playing sounds
import pygame

# Used for Google Cloud Text-to-Speech functionality
from google.cloud import texttospeech

# Used for Google Cloud Speech-to-Text functionality
from google.cloud import speech_v1p1beta1 as speech

# Used to record and play audio with the sounddevice library
import sounddevice as sd

# Used for working with numpy arrays, for example, when processing audio data
import numpy as np

# Used for the Porcupine hotword detection library
import pvporcupine

# Used for working with audio streams using the PyAudio library
import pyaudio

# Used for converting between different data types, for example, when processing audio data
import struct

# Used for creating and managing threads
import threading

# Used for creating and working with deque data structures
from collections import deque

# Used for changing the color and style of terminal output text
from colorama import Fore, Style

#to exit the script
import sys

from threading import Lock
recording_lock = Lock()


# Create a lock for the hotword detection
hotword_lock = threading.Lock()

processing_speech = False


#Initialize the text to speech, speech to text, maps credential json file.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-creds.json"

# Initialize recording variables
recording = False
recorded_audio = []
silence_count = 0
silence_buffer = deque(maxlen=44100)  # Buffer to store the last second of audio samples

# Initialize global voice_enabled variable
voice_enabled = True

# Initialize recording variables
recording = False
recorded_audio = []

found_voice = 0
has_internet = True #for connection status

paused = False # for audio playback

# Initialize global stop_output variable to cease play of mp3 completely. cuts off the ai's speech.
stop_output = False

#LOAD API KEYS#################

# Load API key for openai
with open('openai-key.txt', 'r') as f:
    api_key = f.read().strip()

# Load pvporcupine API key
with open('porcupine-key.txt', 'r') as f:
   PORCUPINE_API_KEY = f.read().strip()

#load user name and info.
with open('my-name-is.txt', 'r') as f:
   my_name = f.read().strip()

with open('about-me.txt', 'r') as f:
   about_me = f.read().strip()

#Describe the ai chatbots role:
some_data = f"You are a helpful assistant.  You sound like a human.  You speak in a condensed way and use less words.  The users name is {my_name}"

# Initialize global stop_hotword_detection variable for bluberry, etc.
stop_hotword_detection = threading.Event()

#detect silence
def is_silent(audio_data, threshold):
    threshold = my_threshold
    global found_voice
    rms = np.sqrt(np.mean(audio_data**2))
    audio_data_dB = 20 * np.log10(rms + np.finfo(float).eps)

    if audio_data_dB < threshold:  # Silence
        print(Fore.GREEN + f"Decibals: {audio_data_dB}" + Style.RESET_ALL)
    else:  # Sound
        print(Fore.YELLOW + f"Decibals: {audio_data_dB}" + Style.RESET_ALL)

    return audio_data_dB < threshold


def recording_thread_function(hotword_activated):
 #   global recording, recorded_audio, record_button
    with sd.InputStream(callback=record_callback, channels=1, samplerate=44100, blocksize=4096):
        if hotword_activated:
            while recording:
                time.sleep(0.1)
            #record_button.config(text="Start Recording")
            sd.stop()
            record_and_transcribe(hotword_activated)
        else:
            while recording:
                time.sleep(0.1)


#PORCUPINE WORD Recognition

global current_task
current_task = ""

def hotword_listen(): #Listen for the activation hotwords, blueberry, terminator, and look-up.
    global current_task
    hotword_lock.acquire()
    while not stop_hotword_detection.is_set():
        porcupine = None
        pa = None
        audio_stream = None

        try:
            porcupine = pvporcupine.create(
                keyword_paths=[pvporcupine.KEYWORD_PATHS["blueberry"],pvporcupine.KEYWORD_PATHS["terminator"], "look-up.ppn"],
                sensitivities=[0.5, 0.5, 0.5],
                access_key=PORCUPINE_API_KEY,
            )
            pa = pyaudio.PyAudio()

            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length,
                input_device_index=None,
            )

            print("Listening for hotword...'blueberry' for ai chat or 'look up' for wikipedia")


            while not stop_hotword_detection.is_set():
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                keyword_index = porcupine.process(pcm)

                if keyword_index >= 0 and not recording:  # Add condition to check if not recording
                    if keyword_index == 0:  # "blueberry" detected
                        print("Blueberry detected!")
                        beep()
                        current_task = "chat"
                        toggle_recording(True)
                        break
                    elif keyword_index == 2:  # "look up" detected
                        print("Look up hotword detected!")
                        # Add your code here
                        current_task = "wikit"
                        #text_to_speech("Looking up wikipedia", "output.mp3")
                        play_mp3_file("look-up-wikipedia.mp3")
                        time.sleep(2)
                        beep()
                        toggle_recording(True)
                        break
                    elif keyword_index == 1:  # "terminator"
                        print("Changing name")
                        play_mp3_file("what-should-i-call-you.mp3")
                        time.sleep(3)
                        current_task= "change-name"
                        beep()
                        toggle_recording(True)
                    #    global stop_output
                    #    stop_output = True
                    #    print("Stop Output")

        except KeyboardInterrupt:
            print("Stopping hotword listening...")
        finally:
            if audio_stream is not None:
                audio_stream.close()
            if pa is not None:
                pa.terminate()
            if porcupine is not None:
                porcupine.delete()



#STT
def record_callback(indata, frames, time, status):
    global recording, silence_count, silence_buffer
    if status:
        print(status, file=sys.stderr)
    if recording:
        recorded_audio.append(indata.copy())

        # Add the incoming audio data to the silence buffer
        silence_buffer.extend(indata.flatten())

        # Check if the entire buffer is silent
        if is_silent(np.array(silence_buffer), threshold=-37.4):  #-40 for the etm 001 microphone # -37.4 for EIM 003
            silence_count += frames
            print(f"Silence count: {silence_count}")
            if silence_count >= 88200:  # 2 second of silence
                recording = False
                beep()
        else:
            silence_count = 0




#STT also
def transcribe_audio(audio_data):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    if response.results:
        transcript = response.results[0].alternatives[0].transcript
        print(f"Transcription: {transcript}")  # Debug print statement
        return transcript
    else:
        print("No transcription results found.")  # Debug print statement
        return None

def save_string_to_file(text,file_name):
    with open(file_name, 'w') as file:
        file.write(text)

#stt
def record_and_transcribe(hotword_activated):
    global recorded_audio, recording_lock
    print("Current task:", current_task)
    # Acquire the lock before processing the audio data
    with recording_lock:

        if len(recorded_audio) > 0:
            audio_data = np.concatenate(recorded_audio, axis=0)
            audio_data = (audio_data * 32767).astype(np.int16).tobytes()

            transcript = transcribe_audio(audio_data)
            if transcript:
                if hotword_activated:
                    if current_task == "chat":
                        print("chatting")
                        send_message(transcript)
                    if current_task == "wikit":
                        bash_script = "russ-wikit.sh"
                        print("accessing wikipedia")
                        subprocess.run(f"bash {bash_script} '{transcript}'", shell=True)
                    if current_task == "change-name":
                        my_name = transcript
                        save_string_to_file(my_name,"my-name-is.txt")
                        play_mp3_file("ill-call-you.mp3")
                        text_to_speech(my_name,"output.mp3")
                        play_mp3_file("output.mp3")


                else:
                    send_message(transcript)
        else:
            # If recorded_audio is empty, return immediately
            return





#more stt
def toggle_recording(hotword_activated):
    print("Toggling")
    global recording, recorded_audio, silence_count, silence_buffer, recording_lock
    silence_count = 0
    silence_buffer = deque(maxlen=44100)  # Buffer to store the last second of audio samples

    with recording_lock:
        if not recording:
            recorded_audio = []
            recording = True
            input_device_index = sd.default.device[0]  # Get the default input device index

            recording_thread = threading.Thread(target=recording_thread_function, args=(hotword_activated,))
            recording_thread.start()

        else:
            recording = False
            sd.stop()
            if hotword_activated:
                hotword_activated = False  # Reset hotword_activated to False after processing

            # Acquire the lock before calling record_and_transcribe
            # Check if hotword_activated is True and restart hotword listening
            if hotword_activated:
                hotword_activated = False  # Reset hotword_activated to False after processing
                hotword_listen()  # Restart hotword listening after processing



# Initialize global chat_history_list
chat_history_list = [
    {"role": "system", "content": some_data}
]

def load_chat_history():
    global chat_history_list
    try:
        with open('chat_history.txt', 'r') as file:
            chat_history_list = json.load(file)
    except FileNotFoundError:
        # If chat_history.txt doesn't exist, create an initial chat_history_list
        chat_history_list = [{"role": "system", "content": some_data}]
        chat_history_list.append({"role": "user", "content": about_me})

def save_chat_history():
    with open('chat_history.txt', 'w') as file:
        json.dump(chat_history_list, file)

def truncate_history(): #keep history file from getting too long
    global chat_history_list

    # Check if chat history list exceeds 15000 characters and truncate if necessary
    chat_history_text = "".join([message["content"] for message in chat_history_list])
    if len(chat_history_text) > 10000:
        excess_chars = len(chat_history_text) - 10000
        for i in range(len(chat_history_list)):
            message = chat_history_list[i]
            content = message["content"]
            if len(content) <= excess_chars:
                excess_chars -= len(content)
                chat_history_list.pop(i)
            else:
                message["content"] = content[excess_chars:]
                break


def play_mp3_file(file_path):
    global stop_output, paused
    stop_output = False
    paused = False
    print("playing audio")
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() and not stop_output:
        if not paused:
            time.sleep(0.1)
        else:
            pygame.mixer.music.pause()
            while paused:
                time.sleep(0.1)
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    stop_output = False



def text_to_speech(text, output_file):
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    #voice = texttospeech.VoiceSelectionParams(
    #    language_code="en-US",
    #    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    #)
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
        print(f'Audio content written to file "{output_file}"')


def send_message(message, event=None):
    #global stop_output
    global chat_history_list  # Access the global chat_history_list variable

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Update the chat_history_list with the user's message
    chat_history_list.append({"role": "user", "content": message})

    # Check if chat history list exceeds 15000 characters and truncate if necessary
    truncate_history()

    data = {
        "messages": chat_history_list,  # Include chat_history_list in the data payload
        "model": "gpt-3.5-turbo"
    }

    API_URL = "https://api.openai.com/v1/chat/completions"
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = response.json()
        ai_message = response_json['choices'][0]['message']['content']

        # Update the chat_history_list with the AI's response
        chat_history_list.append({"role": "assistant", "content": ai_message})

        # Save the updated chat_history_list to the file
        save_chat_history()

        # Only call text_to_speech and play_mp3_file if voice_enabled is True
        if voice_enabled:
            print(ai_message)
            text_to_speech(ai_message, "output.mp3")
            play_mp3_file("output.mp3")

        # Release the hotword_lock if it's acquired
        if hotword_lock.locked():
            hotword_lock.release()
    else:
        print(f"AI: Error: {response.text}")





#computer beep when detect hotword
def beep():
    os.system(f"play -n synth 0.11 sin 880 vol 0.1 ")

def beep_vol(volume):
    os.system(f"play -n synth 0.11 sin 880 vol {volume}")

def detect_hotword(): #for hotwords that you say during the mp3 output: grapefruit, shut up, and stop output.
    global stop_output, paused

    porcupineB = pvporcupine.create(
               #works
               keyword_paths=[pvporcupine.KEYWORD_PATHS["grapefruit"], "shut-up.ppn", "stop-output.ppn"],
               sensitivities=[0.5,0.5,0.5],
               access_key=PORCUPINE_API_KEY,
            )

    pb = pyaudio.PyAudio()

    audio_stream = pb.open(
        rate=porcupineB.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupineB.frame_length,
        input_device_index=None,
    )

    while True:
        pcm = audio_stream.read(porcupineB.frame_length)
        pcm = struct.unpack_from("h" * porcupineB.frame_length, pcm)

        keyword_index = porcupineB.process(pcm)
        if keyword_index == 1 and not recording:  # shutup
            # Stop the 'play' process from sox and play_mp3_file function
            print("Stopping play of mp3")
            beep()
            subprocess.run([f"pkill", "-f", "play"])  # kills the wikipedia lookup output.
            stop_output = True  # stop the mp3 player
        if keyword_index == 2 and not recording:  # 'stop output' pause output
            paused = True
            print("Pausing audio")
            beep()
        if keyword_index == 0 and not recording:  # grapefruit: continue
            if paused:
                paused = False
                pygame.mixer.music.unpause()
                print("Resuming audio")
                beep()



def check_internet(): #threaded, checks for internet connection
    global has_internet
    while True:
        time.sleep(10)
        try:
                # Attempt to resolve the hostname
            socket.gethostbyname("www.google.com")

            # Create a socket and attempt to connect to www.google.com
            s = socket.create_connection(("www.google.com", 80), 2)
            s.close()
            if has_internet == False:
                print("(background:) Internet Connected")
            has_internet = True

        except OSError:
            has_internet = False
            play_mp3_file("no-inet.mp3")
            print("No Internet Connection")


#start listening for keywords LOOK UP and BLUEBERRY and TERMINATOR for change name.
hotword_thread = threading.Thread(target=hotword_listen, daemon=True)
hotword_thread.start()


#load chat chat_history and attempt to trunacte if too long
load_chat_history()
truncate_history()
save_chat_history()

# Run the hotword detection in a separate thread for STOP-OUTPUT, grapefruit, or shutup.
hotword_thread_stop = threading.Thread(target=detect_hotword)
hotword_thread_stop.start()

#Check internet thread
internet_check_thread = threading.Thread(target=check_internet)
internet_check_thread.start()

# Main function
def main():

    #true or false
    global recording

    #add my name to the chat history
    content = f"the users name is {my_name}"
    chat_history_list.append({"role": "user", "content": content})



    print("Starting terminal application...")
    print("Greeting the user")
    text_to_speech(f"Hello {my_name}","output.mp3")
    play_mp3_file("output.mp3")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting terminal application...") #dunno why i have to ctrl-c twice to exit but whatever.
        sys.exit(0)

if __name__ == "__main__":
    main()



#DEV LOG


#Hotword detection during mp3 playback works for the word "stop output"
#say 'look up', wait for beep, say article title, it looks up article using wikit and uses tts to speak the article.  you can say 'stop output'

#Change log

#listens for hotwords 'stop output' and stops.  added if not recroding, so, you cant stop output in the middle of providing input.

#listens for shutup and stops, or stop output and pauses, or grapefruit and continue.
#checks for internet.

#say 'terminator' to change your name.
