import speech_recognition as sr
import os
import pyttsx3
import webbrowser as web
import datetime
import wikipedia
import pywhatkit
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import geocoder
import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speak_utf8(text):
    try:
        text = text.encode('utf-8')
        speak(text)
    except Exception as e:
        print(f"Error during text-to-speech: {e}")

# Use speak_utf8 instead of speak in your code



def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis Sir. Please tell me how may I help you?")
       
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Hmm")
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        r.energy_threshold = 4000  # Adjust energy threshold
        r.pause_threshold = 1
        try:
            print("listening...")
            audio = r.listen(source, timeout=5)  # Set a timeout for speech recognition
            print("recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User Said: {query}")
            return query
        except sr.UnknownValueError:
            print("Could not understand audio")
            speak("I'm sorry, I didn't catch that. Can you please repeat?")
            return take_command()
        except sr.RequestError as e:
            print(f"Error during speech recognition: {e}")
            speak("I encountered an error during speech recognition. Please try again.")
            return "error"

def open_website(url):
    speak(f"Opening{url} sir")    
    web.open(url)

def My_Location():
    speak("Checking....")
    try:
        ip_add = requests.get('https://api.ipify.org').text
        url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
        geo_data = requests.get(url).json()
        city = geo_data.get('city', 'Unknown City')
        state = geo_data.get('region', 'Unknown State')
        country = geo_data.get('country', 'Unknown Country')
        timezone = geo_data.get('timezone', 'Unknown Timezone')

        op = "https://www.google.com/maps/place/" + city
        web.open(op)

        print(f"Sir, you are now in {city}, {state}, {country} and your time zone is {timezone}.")
        speak(f"Sir, you are now in {city}, {state}, {country} and your time zone is {timezone}.")
    except Exception as e:
        print(f"Error fetching location: {e}")
        speak("I encountered an error while fetching your location. Please try again.")


def GoogleMaps(place):
    Url_Place="https://www.google.com/maps/place/"+str(place)
    geolocator=Nominatim(user_agent="myGeocoder")
    location=geolocator.geocode(place,addressdetails=True)
    target_latlon=location.latitude,location.longitude
    web.open(url=Url_Place)
    location=location.raw['address']
    target={'city':location.get('city',''),
            'state':location.get('state',''),
            'country':location.get('country','')}
    current_loca=geocoder.ip('me')
    current_latlon=current_loca.latlng
    distance=str(great_circle(current_latlon,target_latlon))
    distance=str(distance.split('',1)[0])
    distance=str(round(float(distance),2))
    
    speak(target)
    speak(f"sir,{place} is {distance} kilometer away from your location.")
    
def main():
    speak("initializing jarvis")
    speak("all drivers are up and running")
    speak("all system have been activated")
    speak("now i am online")
    speak("Hello, I am Jarvis")
    wish_me()
    while True:
        print("Listening......")
        query=take_command().lower()
        
        if "open youtube" in query:
            open_website("https://www.youtube.com/")
        elif "open google" in query:
            open_website("https://www.google.com/")
        elif "time" in query:
            current_time=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir , The Time is {current_time}")
        elif "wikipedia" in query:
            query=query.replace("wikipedia","")
            results=wikipedia.summary(query,sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
        elif "search youtube".lower() in query:
            query=query.replace("search youtube","")
            speak("search Youtube for"+query)
            pywhatkit.playonyt(query)
            speak("I hope you find what you wre looking for, Sir")
        elif "open in chrome".lower() in query:
            query=query.replace("open in chrome","")
            query=query.replace("jarvis","")
            speak("Searching for"+ query)
            open_website("https://www."+ query)
        elif 'my locaton' in query:
            My_Location()
        elif 'where is' in query:
            Place=query.replace("where is","")
            Place=Place.replace("jarvis","")
        elif "exit" in query:
            speak("Goodbye, Sir")
            exit()
                                                
if __name__=="__main__":
    main()    
    