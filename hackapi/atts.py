import azure.cognitiveservices.speech as speechsdk

# speech_key, service_region = "YourSubscriptionKey", "YourServiceRegion"
#speech_key, service_region = "e982182ae9c6404dbb452c3d6f72e3da", "eastus"
speech_key, service_region = "484f2a1cb1cd45bebef08166c7cd9ebf", "eastus"

class ATextToSpeech:
    name_text = None
    language = None

    def __init__(self, name_text, language):
        print("Inside __init__ function of ATextToSpeech")
        self.name_text = name_text
        self.language = language
        print("Exiting out of __init__ function of ATextToSpeech")

    def convert_to_audio(self):
        print("Inside convert_to_audio function of ATextToSpeech")
        # Creates an instance of a speech config with specified subscription key and service region.
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        # Sets the synthesis output format.
        # The full list of supported format can be found here:
        # https://docs.microsoft.com/azure/cognitive-services/speech-service/rest-text-to-speech#audio-outputs
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

        # The language of the voice that speaks.
        speech_config.speech_synthesis_voice_name = 'en-US-JennyNeural'

        # Creates a speech synthesizer using file as audio output.
        # Replace with your own audio file name.
        audio_file = "output.mp3"
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

        print("Exiting out of convert_to_audio function of ATextToSpeech")
        return audio_file