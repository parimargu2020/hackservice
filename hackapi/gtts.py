"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
import os

GOOGLE_APPLICATION_CREDENTIALS_JSON_PATH = "C:\\Users\\parim\\hackservice\\hackapi\\lucky-essence-349904-adbb34292993.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS_JSON_PATH

class GTextToSpeech:
    name_text = None

    def __init__(self, name_text):
        print("Inside __init__ function of GTextToSpeech")
        self.name_text = name_text
        print("Exiting out of __init__ function of GTextToSpeech")

    def convert_to_audio(self):
        print("Inside convert_to_audio function of GTextToSpeech")
        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        audio_file = None
        audio_file = "output.mp3"

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=self.name_text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open(audio_file, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')

        print("Exiting out of convert_to_audio function of GTextToSpeech")
        return audio_file
