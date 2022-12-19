import gtts  
from playsound import playsound  
import os

def text_to_speech(text:str):
    try:
        gtts.gTTS(text).save("audio.mp3")
        playsound("audio.mp3")   
    except:
        pass
    try:
        os.remove("audio.mp3")
    except:
        pass
