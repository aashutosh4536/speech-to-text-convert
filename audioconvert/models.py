from django.db import models

# Create your models here.
class SpeechToText(models.Model):
    audio = models.FileField(null=True,blank=True,upload_to='speech-to-text-audio/')
    transcript = models.CharField(max_length=2000,null=True,blank=True)