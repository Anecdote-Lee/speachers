# main.py (python example)
from dotenv import load_dotenv
import os
import requests

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

# Path to the audio file
AUDIO_FILE = "./data/example2.m4a"
load_dotenv()
print(os.environ.get("DEEPGRAM_API_KEY"))
def main():
    
    # Define the URL for the Deepgram API endpoint
    url = "https://api.deepgram.com/v1/listen"

    # Define the headers for the HTTP request
    headers = {
        "Authorization": os.environ.get("DEEPGRAM_API_KEY"),
        "Content-Type": "audio/*"
    }
    print(headers)
    # Get the audio file
    with open(AUDIO_FILE, "rb") as audio_file:
        # Make the HTTP request
        response = requests.post(url, headers=headers, data=audio_file)

    print(response.json())
    # try:
    #     # STEP 1 Create a Deepgram client using the API key
    #     deepgram = DeepgramClient()

    #     with open(AUDIO_FILE, "rb") as file:
    #         buffer_data = file.read()

    #     payload: FileSource = {
    #         "buffer": buffer_data,
    #     }

    #     #STEP 2: Configure Deepgram options for audio analysis
    #     options = PrerecordedOptions(
    #         model="nova-2",
    #         smart_format=True,
    #     )

    #     # STEP 3: Call the transcribe_file method with the text payload and options
    #     response = deepgram.listen.rest.v("1").transcribe_file(payload, options)

    #     # STEP 4: Print the response
    #     print(response.to_json(indent=4))

    # except Exception as e:
    #     print(f"Exception: {e}")


if __name__ == "__main__":
    main()


