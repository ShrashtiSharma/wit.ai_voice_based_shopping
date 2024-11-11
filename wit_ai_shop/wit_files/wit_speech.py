import requests
import json
import os
from wit_files.Recorder import record_audio, read_audio

# Wit speech API endpoint
API_ENDPOINT = 'https://api.wit.ai/speech'

# Wit.ai API access token (You can use an environment variable for better security)
wit_access_token = os.getenv('WIT_AI_TOKEN', 'XMK3WRWPX4WQJVIBBA7EMGLBH23XXKXL')


def RecognizeSpeech(AUDIO_FILENAME, num_seconds=5):
    try:
        print("Recording audio...")  # Debug print
        # Record audio of specified length in the specified audio file
        record_audio(num_seconds, AUDIO_FILENAME)

        print("Reading audio...")  # Debug print
        # Read audio data
        audio = read_audio(AUDIO_FILENAME)

        # Defining headers for HTTP request
        headers = {
            'Authorization': f'Bearer {wit_access_token}',
            'Content-Type': 'audio/wav'
        }

        # Making an HTTP POST request to Wit.ai API
        print("Sending request to Wit.ai...")  # Debug print
        response = requests.post(API_ENDPOINT, headers=headers, data=audio)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")  # Debug print
            print("Response content:", response.content.decode())  # Debug print
            return {"error": "Failed to get a valid response from Wit.ai"}

        # Converting response content to JSON format
        data = response.json()
        print("Wit.ai response:", data)  # Debug print

        # Return the recognized speech data
        return data

    except Exception as e:
        print(f"Error in RecognizeSpeech function: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    print("Starting speech recognition...")  # Debug print
    text = RecognizeSpeech('myspeech.wav', 4)
    print("\nYou said:", text)
