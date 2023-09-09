import tempfile
from gtts import gTTS
import speech_recognition as sr
import os
class low_level_stt:
    def text_to_speech(self, text, language):
        # Passing the text and language to the engine, 
        # here we have marked slow=False. Which tells 
        # the module that the converted audio should 
        # have a high speed
        myobj = gTTS(text=text, lang=language, slow=False)
        
        # Create a temporary file to store the audio
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            # Saving the converted audio in a mp3 file
            myobj.write_to_fp(f)
            # Play the audio
            os.system(f"mpg321 {f.name}")
            # Delete the temporary file
            os.unlink(f.name)

    def text_to_mp3(self, text, language):
        # Passing the text and language to the engine, 
        # here we have marked slow=False. Which tells 
        # the module that the converted audio should 
        # have a high speed
        myobj = gTTS(text=text, lang=language, slow=False)
        
        # Create a temporary file to store the audio
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            # Saving the converted audio in a mp3 file
            myobj.write_to_fp(f)
            # Get the path of the temporary file
            path = f.name
        
        return path