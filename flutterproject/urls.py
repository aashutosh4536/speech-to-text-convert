from django.contrib import admin
from django.urls import path
from audioconvert import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('speech-to-text/',views.SpeechToText.as_view())
]
