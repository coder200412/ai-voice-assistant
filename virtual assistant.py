import pathlib
import subprocess
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import time
import platform
import requests
import json
import geocoder
import os
import psutil
from pptx import Presentation
from pptx.util import Inches
import pyautogui
import cv2
from collections import defaultdict
from io import StringIO


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def greet():
    current_time = datetime.datetime.now()
    hour = current_time.hour

    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

def open_chrome():
    subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"])

def close_chrome():
    os.system("taskkill /f /im chrome.exe")
    speak("Chrome has been closed.")

def open_firefox():
    subprocess.Popen(["C:\\Program Files\\Mozilla Firefox\\firefox.exe"])

def close_firefox():
    os.system("taskkill /f /im firefox.exe")
    speak("Firefox has been closed.")

def open_youtube():
    subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", "https://www.youtube.com"])

def close_browser(browser):
    if platform.system().lower() == "windows":
        os.system(f'taskkill /f /im {browser}.exe')
    else:
        speak(f"Sorry, closing {browser} is not supported on this operating system.")

def close_youtube():
    close_browser("chrome")



def open_whatsapp():
    webbrowser.open("https://web.whatsapp.com/")

def close_whatsapp():
    close_browser("chrome")

def open_mail():
    subprocess.Popen(["HxOutlook.exe"])

def close_mail():
    subprocess.run(["taskkill", "/f", "/im", 'HxOutlook.exe'])
    speak("Mail has been closed.")
    
def open_file_explorer():
    system = platform.system().lower()

    if system == "windows":
        subprocess.Popen(["explorer.exe"])
    elif system == "darwin":
        subprocess.Popen(["open", "."])
    elif system == "linux":
        subprocess.Popen(["xdg-open", "."])
    else:
        speak("Sorry, opening File Explorer is not supported on this operating system.")

def open_settings():
    subprocess.Popen(["control.exe", "control"])



def turn_on_bluetooth():
    subprocess.run(["powershell", "Enable-Bluetooth"])

def turn_off_bluetooth():
    subprocess.run(["powershell", "Disable-Bluetooth"])

def connect_wifi():
    ssid = "xxxx"
    username = "xxxx"
    password = "xxxx"
    try:
        speak(f"Connecting to Wi-Fi network {ssid}.")
        subprocess.run(["netsh", "wlan", "connect", "name", ssid], check=True, capture_output=True)
        if username and password:
            subprocess.run(["netsh", "wlan", "set", "profileparameter", f"name={ssid}", "keyMaterial={password}", "authMode=User"], check=True, capture_output=True)
            subprocess.run(["netsh", "wlan", "connect", "name", ssid, "user", username, "keyMaterial", password], check=True, capture_output=True)
        speak(f"Successfully connected to Wi-Fi network {ssid}.")
    except subprocess.CalledProcessError as e:
        speak(f"Error connecting to Wi-Fi: {e.stderr.decode('utf-8')}")

def turn_off_wifi():
    subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "admin=disable"])

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
            return command
        except sr.UnknownValueError:
            print("Could not understand audio.")
            speak("Sorry, I didn't understand that command.")
        except sr.RequestError as e:
            print(f"Google Speech Recognition request failed: {e}")
            speak("Sorry, there was an issue with the speech recognition service.")
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for a phrase to start.")
            speak("Listening timed out. Please try again.")
        return None

def execute_command(command):
    if "open" in command and ("app" in command or "application" in command):
        app_name = command.split(" ", 1)[1]
        open_application(app_name)
    elif "gather" in command and ("data" in command or "information" in command):
        gather_data()

def open_application(app_name):
    try:
        os.system(f"start {app_name}.exe") 
    except Exception as e:
        print(f"Error opening application: {e}")

def gather_data():
    
    print("Gathering data...")

def get_weather(city):
    api_key = 'xxxxxxxxx'
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=ccb23b78c0aafcab3d66f0ca81ea949a&units=metric'
    try:
        response = requests.get(base_url)
        weather_data = response.json()
        if weather_data['cod'] == '404':
            speak('City not found. Please try again.')
        else:
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            speak(f'The current temperature in {city} is {temperature} degrees Celsius with {description}.')
    except Exception as e:
        print(f'Error fetching weather data: {e}')
        speak('Sorry, I encountered an error while fetching the weather.')

def get_current_city():
    try:
        location = geocoder.ip('me')
        return location.city
    except Exception as e:
        print(f"Error getting current city: {e}")
        return None

def get_current_location_weather():
    current_city = get_current_city()
    if current_city:
        speak(f"Checking the weather in {current_city}.")
        get_weather(current_city)
    else:
        speak("Unable to determine the current location. Please try again later.")

def add_city(cities):
    speak("Please tell me the name of the city you'd like to add.")
    new_city = listen()
    cities.append(new_city)
    speak(f'{new_city} has been added to the list of cities.')

def change_location(cities):
    speak("Sure, please tell me the new location.")
    new_location = listen()
    if new_location in cities:
        speak(f"Changing location to {new_location}.")
        get_weather(new_location)
    else:
        speak("Sorry, I don't have weather information for that city.")

def close_weather():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() == 'chrome.exe':
            process.kill()

def main():
    greet()
    while True:
        command = listen()
        if command is not None:
            if "open chrome" in command:
                open_chrome()
            elif "close chrome" in command:
                close_chrome()
            elif "open firefox" in command:
                open_firefox()
            elif "close firefox" in command:
                close_firefox()
            elif "open youtube" in command:
                open_youtube()
            elif "close youtube" in command:
                close_youtube()
           
            elif "open whatsapp" in command:
                open_whatsapp()
            elif "close whatsapp" in command:
                close_whatsapp()
            elif "open mail" in command:
                open_mail()
            elif "close mail" in command:
                close_mail()
            elif "open file explorer" in command:
                open_file_explorer()
            elif "open settings" in command:
                open_settings()
            
            elif "turn on bluetooth" in command:
                turn_on_bluetooth()
            elif "turn off bluetooth" in command:
                turn_off_bluetooth()
            elif "connect wifi" in command:
                connect_wifi()
            elif "turn off wifi" in command:
                turn_off_wifi()
            elif "check weather" in command:
                get_current_location_weather()
            elif "change location" in command:
                change_location(["City1", "City2"])
            elif "add city" in command:
                add_city(["City1", "City2"])
            elif "close weather" in command:
                close_weather()
            else:
                speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    main()
