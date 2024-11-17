import requests
import json
import os
from Recorder import record_audio, read_audio

# Wit speech API endpoint
API_ENDPOINT = 'https://api.wit.ai/speech'

# Wit.ai API access token (Use environment variables for better security)
wit_access_token = os.getenv('WIT_AI_TOKEN', '7KZ7AJ3PVZZ342N2IIUG6ZQDIX6DOG7M')

def RecognizeSpeech(AUDIO_FILENAME, num_seconds=5):
    try:
        print("Recording audio...")  # Debug print
        # Record audio of specified length in the specified audio file
        record_audio(num_seconds, AUDIO_FILENAME)

        # Check if the file is created and has content
        if not os.path.exists(AUDIO_FILENAME):
            print(f"Error: {AUDIO_FILENAME} not created.")
            return {"error": f"Audio file {AUDIO_FILENAME} not created."}

        print("Reading audio...")  # Debug print
        # Read audio data
        audio = read_audio(AUDIO_FILENAME)

        # Defining headers for HTTP request
        headers = {
            'Authorization': f'Bearer {wit_access_token}',
            'Content-Type': 'audio/wav'
        }

        print("Sending request to Wit.ai...")  # Debug print
        # Making an HTTP POST request to Wit.ai API
        response = requests.post(API_ENDPOINT, headers=headers, data=audio)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")  # Debug print
            print("Response content:", response.content.decode())  # Debug print
            return {"error": "Failed to get a valid response from Wit.ai"}

        print("Parsing response...")  # Debug print
        # Try to parse the response as JSON
        try:
            data = response.json()
            print("Response data:", json.dumps(data, indent=2))  # Debug print to show the full response
        except json.JSONDecodeError:
            print("Error: Wit.ai returned non-JSON data")
            print("Raw response content:", response.content.decode())  # Debug print
            return {"error": "Invalid JSON response from Wit.ai"}

        # Extract text from the response
        recognized_text = ""

        # Handling partial and final transcriptions
        if 'text' in data:
            recognized_text = data['text']
            print(f"Recognized Text: {recognized_text}")  # Debug print
        else:
            print("No final transcription text found.")  # Debug print
        
        # Clean up the temporary audio file
        if os.path.exists(AUDIO_FILENAME):
            os.remove(AUDIO_FILENAME)
            print(f"Deleted temporary file: {AUDIO_FILENAME}")

        # Return the recognized speech text
        return recognized_text

    except Exception as e:
        print(f"Error in RecognizeSpeech function: {e}")
        return {"error": str(e)}

# Test the RecognizeSpeech function
if __name__ == "__main__":
    print("Starting speech recognition...")  # Debug print
    recognized_text = RecognizeSpeech('myspeech.wav', 4)
    print("\nYou said:", recognized_text)
