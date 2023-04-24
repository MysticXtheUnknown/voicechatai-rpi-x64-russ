#!/bin/bash

#RUSS SAYS: This script is a helper for the main python script, it runs wikit and speaks the output.

#You shouldnt need to run this seperately but you may need to give it executable and other permissions.

#make sure you are "cd /the/folder/path"

# Check if the argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <search_query>"
    exit 1
fi

# Set your Google API key or the path to your JSON file
export GOOGLE_APPLICATION_CREDENTIALS="google-creds.json"

# Run wikit with the provided argument and capture the output
wikit_output=$(wikit "$1")

# Use gtts-cli to create an mp3 file with the wikit output
echo "$wikit_output" | gtts-cli - -o wikit_output.mp3

# Play the mp3 file using the 'play' command from SoX
play wikit_output.mp3

# Remove the temporary mp3 file
rm wikit_output.mp3
