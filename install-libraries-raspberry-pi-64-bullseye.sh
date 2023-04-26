#!/bin/bash

#THIS WILL INSTALL NECESSARY LIBRARIES FOR RVAC

#DO NOT USE UNLESS USING RASPBERRY PI OS BULLSEYE AS OF APRIL 2023 or later.

#the reason is, other systems like manjaro use pacman, for instance.

#Update your system:
echo "Russ Voice Ai Chat Installing libraries for RPI bullseye x64."
echo "You have ten seconds to cancel. (ctrl+c) before installation begins."
echo "You will have to enter your sudo password a few times probably, during installation"
sleep 10

echo "RVAC: using apt-get update, then apt-get upgrade the system:"
sudo apt-get update
sudo apt-get upgrade

#Install necessary system packages:  Some of these are preinstalled with bullseye.
echo "RVAC: INSTALLING PYTHON3 and PIP"
sudo apt-get install python3 python3-pip

#Install the Google Speech-to-Text and Text-to-Speech packages:
echo "RVAC: INSTALLING GOOGLE TTS and STT libraries"
pip3 install google-cloud-speech google-cloud-texttospeech

#Install pyaudio and required libraries as follows, and in this order:
#(it manages audio streams)

echo "RVAC: INSTALLING pyaudio and requirements"
sudo apt-get install libasound2-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install python3-pyaudio

#Install Porcupine for hotword detection:
echo "RVAC: INSTALLING PVPORCUPINE"
pip3 install pvporcupine

#Install Pygame for playing MP3 files: this may be preinstalled on bullseye.
echo "RVAC: INSTALL PYGAME"
pip3 install pygame

#Install sounddevice for mp3 playback
echo "RVAC: INSTALL SOUNDDEVICE"
pip3 install sounddevice

#Install sox for playing beep sound from terminal command 'play'.  use the regular package manager:
echo "RVAC: INSTALL SOX"
sudo apt-get install sox

#for data management (was already installed on bullseye)
echo "RVAC: INSTALL NUMPY"
pip3 install numpy

#for text color in the terminal (was already installed on bullseye)
echo "RVAC: INSTALL COLORAMA"
pip3 install colorama

#for wikipedia functionality (hotword is 'look up')
echo "RVAC: INSTALL WIKIT"
pip3 install wikit

#this is probably already installed on your system. if its not, this installs it.
echo "RVAC: INSTALL/CHECK FOR REQUESTS LIBRARY"
pip3 install requests

#and finally for sanity reboot the system (save your work first):
echo "RVAC: Done...  You're almost ready to run the chat software."
echo "please refer to readme.txt"
