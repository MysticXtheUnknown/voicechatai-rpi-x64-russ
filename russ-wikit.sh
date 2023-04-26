#!/usr/bin/env bash
#
#RUSS SAYS: This script is a helper for the main python script, it runs wikit and speaks the output.
#
#Shouldn't need to run this seperately, if that's the case, give will need executable permissions.
#If within a python package and installed into a virtual environment, will have the correct permissions
#
#Arg 1 is the search query. Which should be located in the cwd, `cd /the/folder/path`
#
#todo:
# Deal with command failure situations: play, gtts-cli, and wikit.
# These commands when/if they fail, might cause this script to unexpectedly exit.
# What happens when these commands fail?
#      || :
#      ^^ is your friend!
#
#todo:
# Pass in the folder as a script arg. Fallback is cwd
#
# Check if the argument is provided
SCRIPT_NAME=${0##*/}
if [[ -z "$1" ]]; then
    builtin echo "Usage: $SCRIPT_NAME <search_query>"
    builtin exit 1
fi

# Set your Google API key or the path to your JSON file
builtin export GOOGLE_APPLICATION_CREDENTIALS="google-creds.json"

# Run wikit with the provided argument and capture the output
if [[ -x /bin/wikit ]] && [[ -x /bin/gtts-cli ]]; then
    wikit_output=$(/bin/wikit "$1")

    # Use gtts-cli to create an mp3 file with the wikit output
    builtin echo "$wikit_output" | /bin/gtts-cli - -o wikit_output.mp3

    # Play the mp3 file using the 'play' command from SoX
    /bin/play wikit_output.mp3

    # Remove the temporary mp3 file
    /bin/rm -preserve-root wikit_output.mp3
fi
exit 0
