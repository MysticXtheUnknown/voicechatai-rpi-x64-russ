#RUSS SAYS this script prints the decibals on the microphone. choose f)eed or s)ample with enter key.

#runs in the terminal.

# python3 script.py arg1=threshhold arg2=secondstorun
#
#called like this: (threshold is below -37 decibals, and it will run for ten seconds):
#
#   cd /path/to/folder/
#   python3 /path/to/folder/output-decibals.py -37 10
#

#you will be prompted for 'feed' or 'sample'.  Feed continually spits out values, and sample gives a value when you hit enter.  ctrl+c to quit.

#Got an error?  Try installing these libraries:
#
#   pip3 install numpy sounddevice colorama
#

import numpy as np
import sounddevice as sd
import time
import sys
import argparse
from colorama import Fore, Style, init

import statistics

# Global variables to store decibel values
decibel_values = []


# Initialize Colorama
init(autoreset=True)

# Global variable to store the latest audio data
latest_audio_data = None

# Global variables to store highest and lowest decibel values
highest_dB = float('-inf')
lowest_dB = float('inf')

# Function to print the results
def print_results(decibel_values, threshold):
    if not decibel_values:
        print("\nError: No decibel values recorded.  Check your mic is connected and set up properly")
        return

    print("\nResults:")
    print("Highest decibel value: ", max(decibel_values))
    print(" Lowest decibel value: ", min(decibel_values))

    mean_value = np.mean(decibel_values)
    median_value = np.median(decibel_values)
    mode_value = statistics.mode(decibel_values)

    mean_color = Fore.GREEN if mean_value <= threshold else Fore.YELLOW
    median_color = Fore.GREEN if median_value <= threshold else Fore.YELLOW
    mode_color = Fore.GREEN if mode_value <= threshold else Fore.YELLOW

    print(mean_color + "   Mean decibel value: ", mean_value)
    print(median_color + " Median decibel value: ", median_value)
    print(mode_color + "   Mode decibel value: ", mode_value)
    print("            Threshold: ", threshold)


def print_decibels(audio_data, threshold):
    global highest_dB, lowest_dB, decibel_values
    rms = np.sqrt(np.mean(audio_data**2))
    audio_data_dB = 20 * np.log10(rms + np.finfo(float).eps)

    # Update highest and lowest decibel values
    highest_dB = max(highest_dB, audio_data_dB)
    lowest_dB = min(lowest_dB, audio_data_dB)

    # Add the current decibel value to the list
    decibel_values.append(audio_data_dB)

    color = Fore.GREEN if audio_data_dB <= threshold else Fore.YELLOW
    print(color + "Decibels: ", audio_data_dB)

def record_callback(indata, frames, time, status):
    global latest_audio_data
    if status:
        print(status, file=sys.stderr)
    latest_audio_data = indata.copy()

def record_continuous(threshold, duration=None):
    start_time = time.time()
    #decibel_values = []

    with sd.InputStream(callback=record_callback, channels=1, samplerate=44100, blocksize=4096):
        while True:
            if latest_audio_data is not None:
                print_decibels(latest_audio_data, threshold)

            # Exit the loop after the specified duration
            if duration is not None and time.time() - start_time >= duration:
                break

            time.sleep(0.1)

    print_results(decibel_values, threshold)




def record_single_sample(threshold):
    global latest_audio_data
    with sd.InputStream(callback=record_callback, channels=1, samplerate=44100, blocksize=4096):
        while True:
            input("Press ENTER to take a sample. Press CTRL+C to exit.")
            if latest_audio_data is not None:
                print_decibels(latest_audio_data, threshold)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decibel Level Monitor")
    parser.add_argument("threshold", type=float, help="Threshold for decibel level coloring")
    parser.add_argument("duration", nargs="?", type=float, default=None, help="Duration to run the script in seconds (optional)")
    args = parser.parse_args()

    choice = input("Choose an option: (f)eed or s)ample: ")

    try:
        print("Starting continuous feed...")
        record_continuous(args.threshold, args.duration)
    except KeyboardInterrupt:
        print("\nExiting...")
        print_results(decibel_values, args.threshold)

