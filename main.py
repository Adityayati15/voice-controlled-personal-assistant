import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "YOUR_NEWSAPI_KEY"

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        speak("Error: xAI API key not set.")
        return ""
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",
    )
    completion = client.chat.completions.create(
        model="grok-4-fast",
        messages=[
            {"role": "system", "content": "You are a helpful assistant named Jarvis. Give short replies."},
            {"role": "user", "content": command},
        ],
    )
    return completion.choices[0].message.content

def processCommand(c):
    cl = c.lower()
    if "open google" in cl:
        webbrowser.open("https://google.com")
    elif "open facebook" in cl:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in cl:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in cl:
        webbrowser.open("https://linkedin.com")
    elif cl.startswith("play"):
        parts = cl.split(" ", 1)
        if len(parts) > 1:
            song = parts[1]
            if song in musicLibrary.music:
                webbrowser.open(musicLibrary.music[song])
            else:
                speak("Song not found in library.")
        else:
            speak("Which song?")
    elif "news" in cl:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            for article in data.get('articles', []):
                speak(article.get('title', ''))
        else:
            speak("Failed to fetch news.")
    else:
        resp = aiProcess(c)
        if resp:
            speak(resp)
        else:
            speak("I couldn't process your request.")

if __name__ == "__main__":
    speak("Hello, I am Osho...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening …")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            word = recognizer.recognize_google(audio)
            print("You said:", word)
            if word.lower().strip() == "osho":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Jarvis Active …")
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                command = recognizer.recognize_google(audio)
                print("Command:", command)
                processCommand(command)
        except Exception as e:
            print("Error:", e)


