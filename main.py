import os
import openai
import speech_recognition as sr
import webbrowser
import random
import pyautogui
import ibm_watson
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pyaudio

openai.api_key = "YOUR API KEY"
completion = openai.Completion()

def get_greeting():
    prompts = ['best praise message that "JARVIS" an ai name should say to his SIR to start conversation','what is a good praise  message for "JARVIS" an ai name to say his sir and sir name is SIR']
    prompt = random.choice(prompts)
    response = completion.create(prompt=prompt, engine="text-davinci-003", max_tokens=100)
    greeting = response.choices[0].text.strip()
    return greeting

def get_asking():
    prompt = ['write a sentence similar to anything else SIR or let me know what you need help with Sir?'] 
    response = completion.create(prompt=prompt, engine= "text-davinci-003", max_tokens=70)
    asking = response.choices[0].text.strip()
    return asking

def Reply(question):
    prompt=f'SIR: {question}\nJARIVIS: '
    response=completion.create(prompt=prompt, engine="text-davinci-003", stop=['\SIR'], max_tokens=300)
    answer=response.choices[0].text.strip()
    return answer

authenticator = IAMAuthenticator('YOUR IBM TTS API KEY')
text_to_speech = ibm_watson.TextToSpeechV1(
    authenticator=authenticator
)

text_to_speech.set_service_url('YOUR URL')

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=22050, output=True)

#You can even chnage voice

def speak(text):
    response = text_to_speech.synthesize(
        text=text,
        accept='audio/wav',
        voice='en-AU_JackExpressive' 
    ).get_result()
    audio_data = response.content
    stream.write(audio_data)
    
speak(get_greeting())


def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)
    try: 
        query=r.recognize_google(audio, language='en-in')
        print("SIR Said: {} \n".format(query))
    except Exception as e:
        print("Say That Again....")
        speak("Say that again...")

        return "NONE"
    return query

if __name__ == '__main__':
    while True:
        query = takeCommand().lower()
        answer = Reply(query)
        print(answer)
        speak(answer)

        if 'open youtube' in query:
            webbrowser.open("www.youtube.com")
            speak('Opening youtube')
            if 'open google' in query:
                webbrowser.open("www.google.com")
                speak('Opening google')
             if 'open WebwhatsApp' in query:
                webbrowser.open("https://web.whatsapp.com/")
            if 'open Instagram' in query:
                webbrowser.open("www.instagram.com")
                speak('opening Instagram')
            if 'open twitter' in query:
                webbrowser.open("https://twitter.com/")
                speak('here we go SIR')
            if 'bye' in query:
                speak("JARVIS is offline")
                break
           
      
