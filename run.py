import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import requests
import openai
import time

# Set up your API keys
OPENWEATHER_API_KEY = "846c379fd5425453bafb9205c292a5db"  # Replace with your OpenWeather API key
openai.api_key = "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"  # Replace with your OpenAI API key

def speak(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user command and return as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I am listening...")
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            command = recognizer.recognize_google(audio).lower()
            print(f"Command: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please repeat.")
            return "none"
        except sr.RequestError:
            speak("There is an issue with the speech recognition service.")
            return "none"

def get_weather(city):
    """Fetch real-time weather information using OpenWeather API."""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return f"Sorry, I couldn't fetch weather for {city}. Please check the city name."

        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"The weather in {city} is {weather} with a temperature of {temperature}°C."
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return "Sorry, I couldn't fetch the weather at the moment."

def get_answer_from_chatgpt(query):
    """Get an answer from ChatGPT using the updated OpenAI API."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": query}],
            temperature=0.7,
            max_tokens=150
        )
        answer = response.choices[0].message.content.strip()  # Extracting the answer
        return answer
    except Exception as e:
        print(f"Error fetching answer from ChatGPT: {e}")
        return "Sorry, I couldn't fetch the answer at the moment."

def play_song_on_spotify():
    """Open Spotify and play music."""
    speak("Opening Spotify and playing music.")
    os.system("start spotify")  # Open Spotify
    time.sleep(5)  # Wait for the app to open
    # To play a specific song, you can use Spotify's URI scheme.
    # Example: "spotify:track:6rqhFgbbKwnb9MLmUQDhG6" is the URI for a song.
    # Alternatively, you can automate Spotify actions using pyautogui if needed.

def open_cmd():
    """Open Command Prompt."""
    speak("Opening Command Prompt.")
    os.system("start cmd")

def open_gmail():
    """Open Gmail in the default browser."""
    speak("Opening Gmail.")
    webbrowser.open("https://mail.google.com")

def open_file_explorer():
    """Open File Explorer."""
    speak("Opening File Explorer.")
    os.system("start explorer")

def open_settings():
    """Open Windows Settings."""
    speak("Opening Settings.")
    os.system("start ms-settings:")

def open_microsoft_store():
    """Open Microsoft Store."""
    speak("Opening Microsoft Store.")
    os.system("start ms-windows-store:")

def execute_command(command):
    """Execute commands based on user input."""
    if "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "poster" in command:
        speak("Opening Canva.")
        webbrowser.open("https://www.canva.com")  # Add this line to open Canva
    elif "virat kholi" in command:
        speak("king kohli")
        webbrowser.open("https://www.bing.com/search?q=virat+kohli") 
    elif "notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
    elif "spotify" in command:
        play_song_on_spotify()
    elif "whatsapp" in command:
        speak("Opening WhatsApp")
        os.system("start whatsapp")
    elif "microsoft edge" in command or "edge" in command:
        speak("Opening Microsoft Edge")
        os.system("start msedge")
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()
    elif "cmd" in command:
        open_cmd()
    elif "gmail" in command:
        open_gmail()
    elif "file explorer" in command:
        open_file_explorer()
    elif "settings" in command:
        open_settings()
    elif "microsoft store" in command:
        open_microsoft_store()
    elif "play song" in command:
        song_name = command.replace("play song", "").strip()
        if song_name:
            play_song_on_spotify()
        else:
            speak("Please provide a song name.")
    elif "what is" in command or "who is" in command:
        speak("Let me fetch that for you.")
        print("Fetching answer from ChatGPT...")
        answer = get_answer_from_chatgpt(command)  # Get answer from ChatGPT
        if "Sorry" in answer:  # If ChatGPT couldn't fetch an answer
            speak("I couldn't find the answer. Let me search the web for you.")
            query = command.replace("what is", "").replace("who is", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak(answer)  # Speak the response
    elif "search for" in command or "find" in command:
        speak("Searching on the web.")
        query = command.replace("search for", "").replace("find", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
    else:
        speak("Sorry, I cannot do that yet.")

if __name__ == "__main__":
    try:
        speak("Hello, I am Jarvis. How can I help you?")
        while True:
            try:
                user_command = listen()
                if user_command != "none":
                    execute_command(user_command)
            except Exception as e:
                print(f"Error in command execution: {e}")
                speak("An error occurred while processing your command. Please try again.")
    except KeyboardInterrupt:
        speak("Goodbye!")
        exit()
