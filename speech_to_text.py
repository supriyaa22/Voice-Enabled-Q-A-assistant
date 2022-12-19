import speech_recognition as sr



def convert_speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Anything :")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            pass


print(convert_speech_to_text())

