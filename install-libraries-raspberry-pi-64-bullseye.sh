#!/bin/bash

#THIS WILL INSTALL NECESSARY LIBRARIES FOR RVAC

#DO NOT USE UNLESS USING RASPBERRY PI OS BULLSEYE AS OF APRIL 2023 or later.

#the reason is, other systems like manjaro use pacman, for instance.

#Update your system:
print("Russ Voice Ai Chat Installing libraries for RPI bullseye x64.")
print("You have ten seconds to cancel. (ctrl+c) before installation begins.")
print("You will have to enter your sudo password a few times probably, during installation")
sleep 10

print("RVAC: using apt-get update, then apt-get upgrade the system:")
sudo apt-get update
sudo apt-get upgrade

#Install necessary system packages:  Some of these are preinstalled with bullseye.
print("RVAC: INSTALLING PYTHON3 and PIP")
sudo apt-get install python3 python3-pip

#Install the Google Speech-to-Text and Text-to-Speech packages:
print("RVAC: INSTALLING GOOGLE TTS and STT libraries")
pip3 install google-cloud-speech google-cloud-texttospeech

#Install pyaudio and required libraries as follows, and in this order:
#(it manages audio streams)

print("RVAC: INSTALLING pyaudio and requirements")
sudo apt-get install libasound2-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install python3-pyaudio

#Install Porcupine for hotword detection:
print("RVAC: INSTALLING PVPORCUPINE")
pip3 install pvporcupine

#Install Pygame for playing MP3 files: this may be preinstalled on bullseye.
print("RVAC: INSTALL PYGAME")
pip3 install pygame

#Install sounddevice for mp3 playback
print("RVAC: INSTALL SOUNDDEVICE")
pip3 install sounddevice

#Install sox for playing beep sound from terminal command 'play'.  use the regular package manager:
print("RVAC: INSTALL SOX")
sudo apt-get install sox

#for data management (was already installed on bullseye)
print("RVAC: INSTALL NUMPY")
pip3 install numpy

#for text color in the terminal (was already installed on bullseye)
print("RVAC: INSTALL COLORAMA")
pip3 install colorama

#for wikipedia functionality (hotword is 'look up')
print("RVAC: INSTALL WIKIT")
pip3 install wikit

#this is probably already installed on your system. if its not, this installs it.
print("RVAC: INSTALL/CHECK FOR REQUESTS LIBRARY")
pip3 install requests

#and finally for sanity reboot the system (save your work first):
print("RVAC: Done...  You're almost ready to run the chat software.")
print("RVAC: FINISHING THE INSTALL:")
print("RVAC: to finish setting up RVAC, please make sure your api keys (openai, pvporcupine) are in the correct text files, and make sure your credential file from google is in the main folder and renamed 'google-creds.json' and the stt and tts api are enabled at the google cloud site.  If you have other problems, please make sure you own (chown) and maybe permission mod (chmod 777) the whole folder like this:")
print(" ")
print("sudo chmod 777 path/to/folder/*")
print("sudo chown usern:group path/to/folder/* ")
print(" ")
print("RVAC: Before running the main script, make sure your audio input and output is working properly.")
print("RVAC: TO COMPLETE THE INSTALL, PLEASE ALSO 'sudo reboot' once.  and you should be all set to run the voice chat."
print(" ")
print("To use RVAC, run these two commands:")
print(" ")
print("cd path/to/folder")
print("python3 path/to/file/russ-ai-chat-voice.py")
print(" ")
print("RVAC: Good luck on your mission, soldier.  Over and out.")
