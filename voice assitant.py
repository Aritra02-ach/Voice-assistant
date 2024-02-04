# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 16:30:05 2024

@author: achar
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 00:08:31 2024

@author: achar
"""

import pyttsx3 as p
import speech_recognition as sr
import requests
import datetime
import randfacts
import pywhatkit
import pyjokes
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class info():
    def __init__(self):
        service = Service('D:\chromedriver-win64\chromedriver.exe')
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
    def get_info(self, query):
        self.query = query
        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=&explaintext=&titles={query}&format=json"
        response = requests.get(url)
        data = response.json()

        try:
            page_id = list(data["query"]["pages"].keys())[0]
            paragraph = data["query"]["pages"][page_id]["extract"]
            lines = paragraph.splitlines()  # Split into lines
            first_line = lines[0]  # Extract first line
            print(first_line)
            speak(first_line)
        except KeyError:
            print("Article not found for the topic")
            return None


engine=p.init()

rate=engine.getProperty('rate')
engine.setProperty('rate',160)
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
def speak(text):
    engine.say(text);
    engine.runAndWait()
  
def wishme():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        return("Good morning!")
    elif hour>=12 and hour<16:
        return("Good afternoon!")
    else:
        return("Good evening!")


def get_weather(city):
    api_key = "830d5c1d5131079a582be6025abf611e" # Replace with your actual API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    data = response.json()
    
    if data["cod"] != "404":
        main_data = data["main"]
        temperature_kelvin = main_data["temp"]
        temperature_celsius = temperature_kelvin - 273.15  # Convert from Kelvin to Celsius
        humidity = main_data["humidity"]
        weather_desc = data["weather"][0]["description"]
        
        speak(f"The temperature in {city} is {temperature_celsius:.2f}°C with {humidity}% humidity. The weather is {weather_desc}.")
    else:
        return "City not found."
    
today_date=datetime.datetime.now()
r=sr.Recognizer()

speak("Hello!"+wishme()+"I am your voice assistant!")
speak("Today is:"+today_date.strftime("%d")+"of"+today_date.strftime("%B:%Y")+"and it's currently"+today_date.strftime("%H %M"))
get_weather("Bangalore")
speak("How are you?")

with sr.Microphone() as source:
    r.energy_threshold=10000
    r.adjust_for_ambient_noise(source,1.2)
    audio=r.listen(source)
    print("listening")
    text=r.recognize_google(audio)
    print(text)
if any(word in text.lower() for word in ["good", "fine", "what", "about", "you"]):
    speak("I am having a good day too!")


speak("What do you want me to do?")
def command():
    
    with sr.Microphone() as source:
        r.energy_threshold=10000
        r.adjust_for_ambient_noise(source,1.2)
        print("listening...")
        audio=r.listen(source)
        text2=r.recognize_google(audio)
    
    if "information" in text2:
        speak("On which topic you need information?")
        with sr.Microphone() as source:
            r.energy_threshold=10000
            r.adjust_for_ambient_noise(source,1.2)
            print("listening...")
            audio=r.listen(source)
            infor=r.recognize_google(audio)
        speak("searching {} in wikipedia".format(infor))
        assist=info()
        assist.get_info(infor)


    elif "fact" in text2 or "facts" in text2:
        x=randfacts.getFact()
        print(x)
        speak("Do you know that"+x)
    
    elif any(word in text2.lower() for word in ["joke", "jokes", "tell me a joke", "make me laugh"]):

        joke = pyjokes.get_joke()
        engine.say(joke)
        print(joke)
        engine.runAndWait()
        
    else:
        speak("What shall I play?")
        with sr.Microphone() as source:
            r.energy_threshold=10000
            r.adjust_for_ambient_noise(source,1.2)
            print("listening...")
            audio=r.listen(source)
            command = r.recognize_google(audio)
            song=command.replace('play', '')
            engine.say('Playing '+song)
            engine.runAndWait()
            pywhatkit.playonyt(song)
        
while(True):
    command()
    speak("What next can I do for you?")
        



    
    
    