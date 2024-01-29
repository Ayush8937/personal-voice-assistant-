import os
import pygame
import speech_recognition as sr
import google.generativeai as genai

genai.configure(api_key="AIzaSyC-MH45I0zj7O6gyLZWALf2N9tDiArhNXc")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def speak(text):
    voice = "en-US-AriaNeural"

    command = f'edge-tts --voice "{voice}" --text "{text}" --write-media "hello.mp3"'

    os.system(command)

    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load("hello.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(e)

    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()

def take_command():
    r = sr.Recognizer() 
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-us')
        except Exception as e:
            return ""
    return query

# Main program
query = take_command()
print("You said:", query)

while True:
    response = model.generate_content(query)
    print(response.text)
    speak(response.text)
    query = take_command()
