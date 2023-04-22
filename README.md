# voicechatai-rpi-x64-russ
Voice chat with open ai's chatgpt using a raspberry pi (x64) (tested on bullseye).

Required packages:

To install the necessary packages for the libraries used in this software on Raspberry Pi OS Bullseye (x64), follow these steps:

    Update your system:

sudo apt-get update
sudo apt-get upgrade

    Install necessary system packages:

sudo apt-get install -y python3 python3-pip python3-dev libasound2-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg libsdl2-mixer-2.0-0 libsdl2-2.0-0

    Install the Google Speech-to-Text and Text-to-Speech packages:

pip3 install google-cloud-speech google-cloud-texttospeech

    Install the OpenAI GPT-3 package:

pip3 install openai

    Install PyAudio for audio input and output:

pip3 install pyaudio

    Install Porcupine for hotword detection:

pip3 install pvporcupine

    Install Pygame for playing MP3 files:

pip3 install pygame

pip3 install gtts
