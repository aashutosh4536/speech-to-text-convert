from rest_framework import serializers
from .models import SpeechToText


class SpeechtToTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeechToText
        fields = ('audio',)