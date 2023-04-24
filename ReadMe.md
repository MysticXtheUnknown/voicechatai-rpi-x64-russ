# TITLE #

Russell's Voice Ai Chat (RVAC) for chat-gpt, using the openai api.

# DESCRIPTION

an ai voice control tutor using chatgpt 3.5.
by Archaeopteryx

Voice control your chatgpt: no reading, no typing.

For instance, you say, "blueberry, how are you today", it gets the ai response and uses text to speech and you hear: "as a large language model i dont have any feelings, but i'm happy to assist you in any way i can.  How can I be of service?"

Chat with the chatgpt ai using comfort of voice activation, speech to text, and text to speech.  Educate yourself anywhere, anytime.  Be the life of the party.  I dont go to parties.  I write code instead.

Install directions are for raspberry pi bullseye 64 bit.

Developed in April of 2023 by a human using chatgpt 4.0.

# VERSION: 1.0 (approx 50 versions beyond initial prototype) : Functional.

For best results, avoid using in a noisy environment.

()  TESTED AND WORKS ON:

*Raspberry pi zero-2-w running raspberry pi os bullseye x64 as of april 2023
*Raspberry pi 3b       running raspberry pi os bullseye x64 ''
*Steam deck            running manjaro 64-bit, without updating os except for needed packages, from april 2023.

()Tested and could NOT get the voice chat running on:
*pi 3b with most recent 32 bit raspberry pi os as of april 2023.

# Tested/Recommended OS:
raspberry pi os bullseye x64 or manjaro x64



()-----------TO INSTALL: (raspberry pi os bullseye)

## Theres a script to install the required packages, or you can do it manually.

## RVAC does not install itself into your system at all.  it just installs the needed libraries to the system and runs from it's own folder.

## You do not need to install the openai library, we use the request library instead, so openai is not listed below.

## be sure you do not do 'sudo pip3' to install the packages, as those libraries installed that way cannot be found by the regular user running my main script without 'sudo'.


########## INSTALLING on raspberry pi

###### INSTALL SCRIPT: You can skip some steps and continue at 'FINISH INSTALL', if you want to, by running the install script: (pay attention: NOT 'sudo').

#make sure you are internet connected.

#Look at the script before you run it.

cd /path/to/rvac
sudo nano install-libraries-raspberry-pi-64-bullseye.sh
(ctrl+s to save, ctrl+x to exit nano.)

#run the install script:

cd /path/to/rvac
bash install-libraries-raspberry-pi-64-bullseye.sh

(you'll need to enter your sudo password if/when prompted on the terminal, possibly multiple times)

###### *OR* MANUAL INSTALL:

#or you can install the libraries yourself for raspberry pi as follows:

#Open a terminal. (ctrl+alt+t)

#make sure you are internet connected

#Update your system:

sudo apt-get update
sudo apt-get upgrade

#Install necessary system packages:  Some of these are preinstalled with bullseye.
sudo apt-get install python3 python3-pip

#Install the Google Speech-to-Text and Text-to-Speech packages:
pip3 install google-cloud-speech google-cloud-texttospeech

#Install pyaudio and required libraries as follows, and in this order:
#(it manages audio streams)

sudo apt-get install libasound2-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install python3-pyaudio

#Install Porcupine for hotword detection:
pip3 install pvporcupine

#Install Pygame for playing MP3 files: this may be preinstalled on bullseye.
pip3 install pygame

#Install sounddevice for mp3 playback
pip3 install sounddevice

#Install sox for playing beep sound from terminal command 'play'.  use the regular package manager:

sudo apt-get install sox

#for data management (was already installed on bullseye)
pip3 install numpy

#for text color in the terminal (was already installed on bullseye)
pip3 install colorama

#for wikipedia functionality (hotword is 'look up')
pip3 install wikit

#for the requests library, if you dont have it.  does nothing if you already have it.

pip3 install requests

#and finally for sanity reboot the system (save your work first):
sudo reboot

()------------FINISH THE INSTALL:

#Get api keys and put in appropriate files, replace the '#########' (etc) in the file with your api key.

you'll want to make sure openai-key.txt and porcupine_key.txt contain their appropriate api keys.  porcupine as in pvporcupine (hotword detection)

#get the google cloud credentials for text to speech and speech to text:

you'll need to go to the google cloud developer site.  you'll need to enable both speech to text and text to speech api, then you need to create and download the .json credentials file.  Use google or openai for a tutorial on how to do this.  put it in the RVAC software's folder and rename it "google-creds.json".  A dummy file is there now.

#Make sure your Mic and Headphones are properly configured and connected.

#you might want to chown and chmod the whole folder if you get any errors:

#own the folder contents, inserting your username and group:

sudo chown username:group path/to/folder/*

#add all permissions to folder contents:

sudo chmod 777 path/to/folder/*





() -------------HOW TO USE

optional: fill the my-name-is.txt and about-me.txt with some info (a paragraph is sufficient for about-me.  this is sent to the ai.

#open the terminal on your raspberry pi (shortcut ctrl+alt+t) and execute:
#note: not using sudo here.

cd /path/to/the/RVAC/folder/
python3 russ-ai-chat-voice.py

#if all the libraries are installed, you should see the text "Listening for keyword" without any errors.

#hotwords while waiting for input are blueberry (for regular ai chat), and 'look up' for a wikipedia query.

#hotwords while the audio is playing are 'stop output' (pauses), 'grapefruit' (resume) and 'shut up' to end audio playback and go back start.

at this point you can say "blueberry", wait for beep, then speak your message to the ai.  You can see decibal values in the terminal at this point.  You need to change the my_threshold variable (at the beginning of russ-ai-chat.py) to a value appropriate to your microphone.  Look at the values and choose one somewhere in the middle.  With a couple tries and you'll have it right.  When the decibal is below the threshold, the system detects silence.  after two seconds of silence, the message is turned to text and sent to chat gpt (youll hear another beep when recording ends.).  This can be difficult to use or fix in a noisy room, keep in mind.

Or you could have said "look up", wait for a beep, and then provide the title for a wikipedia article (e.g. 'dog').  the voice to text will read out the condensed article.  This requires no ai, it's just text to speech.

if you say 'terminator', it will ask you what your name is, and it will beep.  you can say 'russ'. or you can just edit my-name.txt and avoid the 'terminator' hotword.

need to pause the article? just say 'stop output'.  need to resume?  say 'grapefruit'.  want to cut off the audio and loop back to detecting the first hotwords?  say 'shut up'.  these three commands only work during the audio playback.  'shut up' kills the audio playback and returns the code to waiting for you to say 'blueberry' etc.

pkill returns an error, ignore it for now.





() LIMITATIONS

() limited ai memory of the conversation

#Yes, api calls are not part of a 'conversation'.  eventually the conversation history gets too big to be passed back to the ai entirely, so, even if you provide your name and about info, it will eventually get truncated away as the oldest parts of the conversation are forgotten.  Delete the chat_history and restart RVAC to start over.

#However, this app is still super useful for self-education and checking wikipedia, neither of which requires the ai to problem solve or have much of a memory.




()POTENTIAL USES

I have this running on a pi zero 2 w (64 bit) with bullseye.  it's taped to a battery. i use vnc on the android phone (app bVNC) to view the desktop.  mostly it just runs my software and i carry it in my pocket and wear my bluetooth earpiece.  Since I logged it into my phone hotspot, it ALWAYS joins my phone hotspot when it becomes available.  I call it my ai tutor.  ive learned a lot of random stuff so far!!  It's not auto-gpt but it's pretty fun to use.  It's an alternative to a heads-up display on your face and interference with your vision from that.

Also rvac would be good for blind people.




()OTHER SCRIPTS INCLUDED on this git:

#russ-ai-terminal-chat.py
(a really simple chat with ai on the terminal. requires an openai api key but not the other api keys.  put your key in openai-key.txt, use keyboard and a display or cell phone remote desktop. 79 lines of code.) this will run on "raspberry pi zero w" with a 32 bit os. it also needs less libraries (requests and json only) which are probably already installed on your system.  This simple chat will work on most systems, and since its only 80 lines, you can easily modify it and it's super easy to get running on your system  because it uses only two libraries and *NOT* the openai api library.

to run:

cd /path/to/rvac
python3 /path/to/rvac/russ-ai-terminal-chat.py

#output-decibals.py
(outputs the decibal levels read on your microphone to the terminal.  if the values are all the same, you're mic is not properly configured and is giving no input to the software. 130 lines of code.)  For a testing microphone decibal threshold of -37 for a maximum of 10 seconds.  If you press f for feed it will spit out lots of values, if you select sample it will only print a value when you press enter. call like this:

python3 path/to/file/output-decibals.py -37 10

#print-porcupine-words.py
(outputs the built in keywords that pvporcupine can respond to.  2 lines of code.)

#text-to-mp3.py
(for dev use, creates an mp3 file of the text you specify in the variable, uses google text to speech api and json credentials from the folder)

FOR ALL ABOVE SCRIPTS please make sure the terminal is in the correct folder by using 'cd /path/to/RAVC', in general this is a good way to avoid script errors if something isnt working otherwise.




()LICENSE:

The user of this software accepts any costs associated with API keys, memberships, and fees for api access.  No keys are provided.  No guarantees about economic or low token usage are given.

do whatever you want, however, porcupine has it's own license in the license folder so be aware if you alter and redistribute ppn files.

do give me credit (Archaeopteryx) in your readme and include 'about the original author' as it appears later in the document with my book info.

This software is provided for free, and NO WARANTEE is expressed, implied or granted.  You use this software at your own risk, and the original author russ is not responsible or liable for any damages or data loss, or loss of property, sanity, data leak, etc.

No guarantees about the security of this code, the security of the data being transmitted, etc.  not recommended for commercial projects.  I dont know anything about encryption.  Please review the code making up the main script before running it.

Please use at your own discretion and take responsibility for your actions and their consequences.  Please consider what data you are sending and only use trusted internet connections.

this code can be reproduced in any form in full or in part, without my permission.  Go crazy.

if you make money with all or a portion of this code by selling or repackaging it, 1% of your profits from the sale of the product containing the code will go to the charity New Hope For Women in Belfast, Maine, USA.

By using or altering, or redistributing this software, you accept this agreement.

#NOTE: if redistributing, make sure to check the pvporcupine license.  last i checked it was Apache 2.0 in april of 2023.





()ABOUT RVAC (Russ Voice Ai Chat)

chat gpt 4.0 wrote most of the code.  I developed it on a manjaro install on my steam deck.  I ended up learning python and modding the code manually for some things.  However I'll say that per line, the ai provided 95% of the code to make RVAC.  I already knew lua and python is extremely similar.  It took me two weeks to develope this software with the help of the ai.  Without ai it would have taken me several months, if not more, with a lower guarantee of actually completing the project. Now I am amateur level with python.

()About the original author Archaeopteryx (russ)

I am a mystic, programmer, aquarist, insect keeper, and jack of all trades.  i am funny, polite, and spiritually complete.  I have bipolar and adhd.  I like guppies, mollies, isopods, and coding.  I am freindly and tend towards a positive mood.  I have 30 credits towards a psychology degree, and I am a published author (from a real publishing company) of a book on Mysticism.  At one point i published twelve apps on the galaxy watch store when it was still Tizen based.  I am pro-social.

I have lost my mind 14+ times, i lost count.  Five years ago was what I call 'the summer of three bluepapers' and i lost alot of vitality.  I'm still recovering.  Life is really good, i will probably be healthy the rest of my life.  I am 41 years old and retired.  I am married.

The book is "A Mystic in Maine: a guide to self-knowledge, by Russell Yates."  If you like it, leave me a review. the book is not perfect but has a lot of good in it.  It's 100% human written, from a time before text completion ai.

()BUGS
report bugs to russell.ackerman.rocketship@gmail.com
no guarantee that I'll fix them.  This is a functional prototype and I am a hobby coder with other responsibilties (roly polys, cats, wife, daughter, stayin alive, smoking cigarettes, etc).

()DONATIONS
Send a check to the charity New Hope for Women, 6 Public Safety Way, Belfast, ME 04915
New Hope For Women provides services to women in Maine who are victims of domestic violence or need community support.
https://domesticviolence.org/maine/waldo/belfast/new-hope-for-women-belfast/

()USING CODE IN OTHER PROJECTS OR REDISTRIBUTING
please let me know what youre up to so i can share the fun.  russell.ackerman.rocketship@gmail.com
no scammers please, and i dont share personal info or click links.

()FINAL WORD
good luck on your mission, soldier!
move out!

()Steam Deck Warning for manjaro x64 linux kde desktop
if you install a new instance of manjaro on your steam deck, running sudo pacman -Syu should have updated my system but it instead bricked my install and it would not show up in the steam deck boot menu anymore.  I reinstalled manjaro three times that day, updated, bricked, before i isolated wtf i was doing.  regardless, you shouldnt have to update manjaro to use this software with the manjaro ppn files on your steam deck.  The 'steam os linux desktop' wont let your (installed packages) changes persist.  use a fresh and seperate manjaro x64 install.  it should be fine, probably you dont need to update anything.




-------------------------------




()TROUBLESHOOTING/ FAQ:

#Help! How do I exit?
just go to the terminal and hit ctrl-c twice.  i might fix that in a future version.

--#Help, somethings wrong!  I'm getting terminal errors:

We can make sure we own all the files and have full permissions. replace usern:group with your username and group (check a file that you own for user and group names)

#own the folder contents:

sudo chown usern:group path_to_folder/*

#add all permissions to folder contents:

sudo chmod 777 path_to_folder/*

#make sure you are internet connected!

#Help!  mic not working?  make sure your devices (microphone, headphones or bluetooth earpiece with microphone) are working properly.  (try h2p instead of a2dp.).  I've tested this with both usb sound card and plantronics voyager bluetooth earpiece.  Galaxy buds are sound only.

#Help! It records forever.

why: it's not detecting 2 seconds of silence below your set threshold.

fix: your my_threshold is too low. Raise it.  look at the beginning of the russ-ai-chat.py.  change my_threshold to a value appropriate for your microphone.  To see some of these values, just say blueberry and look at the terminal output as the decibal levels change when you speak.  A value somewhere in the middle of those values should be a fine place to start.  You should be able to tweak this and get it working comfortably relatively easily.

#Help! It detects silence too quickly and stops when im speaking.

fix: raise your my_threshold variable so while you are speaking, it's not detecting silence.

#Help!  I'm using too many tokens!
solution: edit the code and remove or nerf the chat_history stuff.

#Help! It says im using too many tokens in my request.

you are probably giving it a long verbal request and the chat history is also full.

solution: edit the code and or remove or nerf that chat_history stuff.  Or, make shorter verbal requests. you could probably just comment out any chat_history.append calls and that would roughly do it. i think theres 2 or 3 calls of that.

#Help! It forgot my name!

this happens when the conversation history gets long.  you can (exit first, then) just delete chat_history.txt, it will be rebuilt with your about-info and name on the next run.

Help! I don't know python but i want to change your code!
feed it to the ai at openai.com and tell it what you want to change.  Keep your old versions.  each time you have a functional prototype, back it up.  Use the gpt 4.0 chat if you can, it writes better code, but you have to pay the monthly fee.

#Help!  It looks like I'm missing a library!

I tried to make sure all libraries are accounted for but it's possible i missed one in the install list.  Or, you are trying to run this on an OS i havent tested it on. in that case:

go ahead and copy the beginning of the code (all import statements) to your clipboard and pasting it into chatgpt 4.0.  tell it what os and hardware you are using and ask the ai to run you through how to install the libraries.  alternatively, if the main script outputs an error, by looking at the error output you can often figure out what library you are missing and just ask ai how to install for that one.  www.openai.com.  ALternatively, you can copy and paste the error from the terminal into chatgpt and ask it what packages you are missing. keep in mind her knowledge is limited to <= the year 2021.

#Help with linux?
ask chat gpt. tell it what os and what hardware you are using.

#Help, my mic is working but it wont detect my hotwords very well.

Solution: Look at the sensitivity weights (0.5, 0.5, 0.5) for the blueberry and other hotwords.  i think if you increase these to make the hotword detection more responsive.

#Help! I like your software but i dont like the hotwords youve chosen.

solution: sign up for pvporcupine and generate your own, and or use words that are included with pvpporcupine (siri, ok google, jarvis etc). Then alter the hotword functions (search for 'blueberry' or 'grapefruit' to find the two different hotword functions in the code)

In future versions i will be training more words using pvporcupine but right now i could only train afew because of the monthly limit.  You can train your own though at the pvporcupine console, online.

()FURTHER HELP:

#bluetooth giving you trouble? try blueman (gui) to manage your bluetooth connections and set devices as hands-free (h2p).

sudo apt-get install blueman
sudo reboot

#and to remove,

sudo apt-get remove blueman
sudo reboot

#having trouble with the audio controls?

sudo apt-get install pavucontrol

#and to remove,
sudo apt-get remove pavucontrol
sudo reboot

#and from the command line to use pavucontrol:

pavucontrol

#make sure your mic is recieving input. good luck.

#and finally, when in doubt, reboot and try to run the main script again:

sudo reboot

#other hardware, os: I am mediocre at linux and was able to get this running on three different machines.  you can probably adapt it to your OS but you're on your own.




()VARIOUS

This should fit, with installed libraries, with bullseye, on a 16gb sd card (or smaller, idk).

The voice is one of the female voices, but if you know what you're doing, you can change it in the code. look for '"en-US-Wavenet-F' text in the code.

#it uses chat gpt-3.5 engine. will it work with 4.0?
if you have openai gpt-4.0 api access, you can alter the code to use that model theoretically by changing the 'model' keyword in the send_message function.  check the openai api documentation for the correct string for gpt 4.  you will need the special api permission from filling out the form on their site. and then you wait.

#why raspberry pi?
answer: it's easy to configure vnc server.  I couldnt configure vnc on manjaro *sheepishly*

#What microphone to use?

Edutige eim-003 or plantronics voyager bluetooth earpiece are both tested on pi. galaxy buds dont work for audio input on pi or steam deck.  Other microphones should work, you need to adjust my_threshold variable in the russ-ai-chat.py script after you confirm the microphone is working.  (pavucontrol can be good for configuring the mic)

#MY mic plugged into the audio jack of my pi 3b wont work!
yup.  pi 3b audio jack is output only. use a usb sound card (10$ on amazon) or a bluetooth earpiece.  Plantronics voyager bt earpiece works for input and output.  Set it as hands-free (h2p) using your os' gui, blueman, or console commands.

#Galaxy Buds? The microphone does NOT work on linux without complex tutorial so, you're on your own if that's what you're into.  I couldn't get my galaxy buds to do anything but play audio, no mic.

#Can i run this on another system?  Manjaro?

I've tested it on manjaro and included the ppn files, copy the files from the folder manjaro-porcupine-words into the main folder and rename them as the original ppn files are named.  I was running this on my steam deck using a seperate manjaro install. See the bottom of this document.


#sidenotes:

Now, you could use this code to make a more powerful assistant, capable of running os commands, or as a prototype interface for a blind person.  you could have this app issuing shell commands to shell gpt, or you could write them into one piece of software.

Or, using a raspberry-pi-zero-w (not #2), 32 bit os, you can run my script russ-ai-terminal-chat.py.  Use a waveshare 1.3 inch screen.  You can mount it on your arm with an altoid tin and a cloth arm sleeve with a hole in it.  Use a bluetooth keyboard to chat with the ai.  Its not voice but it will work on the older systems.  and the end result is extremely steam punk.  Put the battery in your pocket and run a usb cord up your sleeve and down into your pocket.  It's cumbersome but it's better than no chat at all since the rpi-zero-w is not powerful enough to really run firefox at all for chatgpt.

This project took me about two weeks, and i have never programmed in python, but, the result is i am editing the code and working with python effectively. if i have questions about syntax i can ask chatgpt.  If I need a function rewritten with a new feature, i paste in my code and i ask chatgpt to add the feature 90% of the time.  Because of my familiarity with lua, python was easy to look at.  If you want to learn to code, chatgpt is the way to do it. no more googling tutorials and pasting unknown console commands. chatgpt is not perfect but is a really excellent tool.

RVAC has super-cow powers.  You just need to program them yourself.
