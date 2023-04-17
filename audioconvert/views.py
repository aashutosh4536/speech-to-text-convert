from django.shortcuts import render
from rest_framework import generics
from .serializers import SpeechtToTextSerializer
from .models import SpeechToText
from rest_framework import status
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import collections 
import os, io, subprocess, wave
from google.cloud import speech_v1 as speech

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = "/home/hp/Downloads/credential.json"

def speech_to_text(config, audio):
    client = speech.SpeechClient()
    response = client.recognize(config=config, audio=audio)
    transcript = print_sentences(response)
    return transcript


def print_sentences(response):
    for result in response.results:
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
        confidence = best_alternative.confidence
        return transcript

 
class SpeechToText(generics.UpdateAPIView):
    serializer_class = SpeechtToTextSerializer

    def post(self, request):
        serializer = SpeechtToTextSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # breakpoint()

                myfile = serializer.validated_data.get('audio')
                fs = FileSystemStorage()
                file_name = fs.save(myfile.name, myfile)
                path=fs.url(myfile)
                full=str(settings.BASE_DIR)+path
                uploaded_file_url = fs.url(file_name)

                src = "/home/hp/speechApp/flutterproject/media/"+str(myfile)
                filepath =f"/home/hp/speechApp/flutterproject/output/{myfile}.wav"
                
                if os.path.exists(filepath):
                    os.remove(filepath)
                else:
                    print("The file does not exist")
                
                subprocess.call(['ffmpeg', '-i', src,
                            filepath])
                    
                dst = filepath
                
                with wave.open(dst, "rb") as wave_file:
                    # frame_rate = wave_file.getframerate()
                    channels = wave_file.getnchannels()
                    channel = channels
                    print("*"*30,channel)
                    # print("*"*30,frame_rate) 
                
                config = dict(
                    language_code="en-US",
                    encoding = "LINEAR16",
                    enable_automatic_punctuation=True,
                    enable_word_time_offsets=True,
                    # model="default"
                    audio_channel_count = channel,
                    enable_separate_recognition_per_channel = True,
                    # useEnhanced=True,
                    # is_final=False,

                )
                
                with io.open(dst, "rb") as audio_file:

                    content = audio_file.read()
                    audio = speech.RecognitionAudio(content=content)
                    transcript = speech_to_text(config, audio)

                
                #with open(f"/home/hp/Projects/flask/proman/proman/transcript/{myfile}.txt", "a") as f:
                with open(f"/home/hp/speechApp/flutterproject/transcript/{myfile}.txt", "a") as f:
                    print(transcript, file=f)
                
                #show_file = "/home/hp/Projects/flask/proman/proman/transcript/{myfile}.txt"
                show_file = "/home/hp/speechApp/flutterproject/transcript/{myfile}.txt"
                
                sentence = transcript
                words = sentence.split()
                word_counts = collections.Counter(words)
                print(words)
              
                serializer.save()

               
                response = {
                        "status": True, 
                        "code": status.HTTP_200_OK, 
                        "message":"Successfully",
                        "errors": [],
                        "payload":serializer.data,
                        "transcript":transcript,
                }
                return Response(response)

            except AttributeError as e:
                response = {
                        "status": "Audio file not found", 
                        "code": status.HTTP_400_BAD_REQUEST, 
                        "message":"Audio file not found",
                        "errors": [],

                    }

                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)