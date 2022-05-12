from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import NameSerializer
from .models import NameModel
from .gtts import GTextToSpeech
from .atts import ATextToSpeech


class NameViews(APIView):
    def post(self, request):
        print("Inside post function of NameViews")
        data = request.data
        name_text = data.get('name_text')
        print("name_text: " + name_text)
        print(data)
        audio_file_path = "/home/azureuser/hackathon/hackservice/"
        audio_file = "output.mp3"

        # Google Cloud Text to Speech API
        #gtts = GTextToSpeech(name_text)
        #audio_file = gtts.convert_to_audio()

        # Azure Cloud Text to Speech API
        language = 'en'
        atts = ATextToSpeech(name_text, language)
        audio_file = atts.convert_to_audio()

        data['audio_file'] = audio_file_path + audio_file

        serializer = NameSerializer(data=data)
        if serializer.is_valid():
            name_text = serializer.validated_data.get('name_text')
            print(name_text)
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
