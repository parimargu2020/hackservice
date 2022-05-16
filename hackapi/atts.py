import azure.cognitiveservices.speech as speechsdk
from azure.storage.blob import BlobServiceClient, BlobClient

# speech_key, service_region = "YourSubscriptionKey", "YourServiceRegion"
#speech_key, service_region = "e982182ae9c6404dbb452c3d6f72e3da", "eastus"
speech_key, service_region = "484f2a1cb1cd45bebef08166c7cd9ebf", "eastus"
AZURE_STORAGE_CONNECTION_STRING_STR = "DefaultEndpointsProtocol=https;AccountName=hackathonsg;AccountKey=+x+D6pN0cQn/s/Q524LY0SbJFyhQacOJVxRNIOLO+gAJF8vowrECBFaQjDsreyiFd5seQwuyno3/+AStWyQxhg==;EndpointSuffix=core.windows.net"

#language_dict = {'us-EN': ['JennyNeural', 'ChristopherNeural'], 'us-IN': []}

class ATextToSpeech:
    name_text = None
    language = None
    voice_name = None
    std_ctm_pronunciation = None
    speaking_style = None
    speaking_speed = None
    speaking_picth = None

    def __init__(self, name_text, language, voice_name, std_ctm_pronunciation):
        print("Inside __init__ function of ATextToSpeech")
        self.name_text = name_text
        self.language = language
        self.voice_name = voice_name
        self.std_ctm_pronunciation = std_ctm_pronunciation
        print("Exiting out of __init__ function of ATextToSpeech")

    def convert_to_audio(self):
        print("Inside convert_to_audio function of ATextToSpeech")
        blobServiceClient = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING_STR)

        # Creates an instance of a speech config with specified subscription key and service region.
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        # Sets the synthesis output format.
        # The full list of supported format can be found here:
        # https://docs.microsoft.com/azure/cognitive-services/speech-service/rest-text-to-speech#audio-outputs
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

        # The language of the voice that speaks.
        # language
        #speech_config.speech_synthesis_language = "en-US"
        speech_config.speech_synthesis_language = self.language
        # language + voice
        #speech_config.speech_synthesis_voice_name = self.language + '-' + self.voice_name
        speech_config.speech_synthesis_voice_name = self.voice_name

        # Creates a speech synthesizer using file as audio output.
        # Replace with your own audio file name.
        audio_file = self.name_text.lower().replace(' ', '-') + '-' + self.std_ctm_pronunciation.lower() + ".mp3"
        audio_file_config = speechsdk.audio.AudioOutputConfig(filename=audio_file)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_file_config)

        result = speech_synthesizer.speak_text_async(self.name_text).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}], and the audio was saved to [{}]".format(self.name_text, audio_file))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

        container_name = "hackaudios"
        # Create a blob client using the local file name as the name for the blob
        blobClient = blobServiceClient.get_blob_client(container=container_name, blob=audio_file)

        print("\nUploading to Azure Storage as blob:\n\t" + audio_file)

        # Upload the created file
        with open(audio_file, "rb") as data:
            blobClient.upload_blob(data, overwrite=True)

        audio_file_url = blobClient.url
        print(audio_file_url)

        print("Exiting out of convert_to_audio function of ATextToSpeech")
        return audio_file_url