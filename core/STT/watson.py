import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Create a microphone instance
microphone = sr.Microphone()

# Adjust for ambient noise
with microphone as source:
    print("Adjusting for ambient noise...")
    recognizer.adjust_for_ambient_noise(source, duration=5)
    print("Ready!")

# Real-time recognition loop
with microphone as source:
    print("Speak something...")
    while True:
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_sphinx(audio)
            print("You said:", text)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
