import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Create a microphone instance
microphone = sr.Microphone()

# Houndify API configuration
HOUNDIFY_CLIENT_ID = "c7sQI8l8RbF8mjgQecGGqg=="
HOUNDIFY_CLIENT_KEY = "h5LHwreH66diFNkCoeOvu-8o7CKwK2aRc3_hM_t8pIzYEZWNA0V3IU-HMPWvT_FY8x-0MNMdKxvBypi0eEwbyQ=="

# Real-time recognition loop
with microphone as source:
    print("Speak something...")
    while True:
        try:
            print("Microphone is on. Speak now...")
            audio = recognizer.listen(source)
            text = recognizer.recognize_houndify(
                audio,
                client_id=HOUNDIFY_CLIENT_ID,
                client_key=HOUNDIFY_CLIENT_KEY
            )
            print("You said:", text)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
