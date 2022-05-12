from rest_framework import serializers
from .models import NameModel


class NameSerializer(serializers.ModelSerializer):
    name_text = serializers.CharField(max_length=100)
    audio_file = serializers.CharField(allow_blank=True)

    class Meta:
        model = NameModel
        fields = ('__all__')