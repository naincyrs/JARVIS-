import os
import webbrowser
import subprocess
import pyttsx3
import sounddevice as sd
import speech_recognition as sr
import io
from scipy.io.wavfile import write
import spacy

# Initialize spaCy and TTS engine
nlp = spacy.load("en_core_web_sm")
engine = pyttsx3.init()

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen to a command and convert it to text using sounddevice and SpeechRecognition."""
    recognizer = sr.Recognizer()

    # Set up audio stream with sounddevice
    fs = 48000  # Sample rate (standard for most devices)
    duration = 5  # Time to listen for a command
    print("Listening...")

    # Record audio using sounddevice
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished

    # Convert the audio to WAV format using scipy
    audio_wav = io.BytesIO()
    write(audio_wav, fs, audio_data)

    # Convert WAV to AudioData using SpeechRecognition
    audio_wav.seek(0)  # Reset the pointer to the start of the byte stream
    audio = sr.AudioData(audio_wav.read(), fs, 2)

    # Use SpeechRecognition to recognize the speech
    try:
        command = recognizer.recognize_google(audio)
        print(f"Recognized command: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return None

def parse_command(command):
    """Parse the command using spaCy."""
    doc = nlp(command)
    intent = None
    entities = {}

    # Detect intent
    if "open" in command:
        intent = "open"
        if "spotify" in command:
            entities["application"] = "spotify"
        elif "opera gx" in command:
            entities["application"] = "opera_gx"
        elif "youtube" in command:
            entities["application"] = "youtube"
        elif "gmail" in command:
            entities["application"] = "gmail"
        elif "vs code" in command :
            entities["application"] = "vs code"
        elif "settings" in command :
            entities["application"] = "settings"
        elif "one note" in command :
            entities["application"] = "one note"
        elif "discord" in command :
            entities["application"] = "discord"

    elif "play" in command and "spotify" in command:
        intent = "play_song"
        # Extract song name by splitting at 'play' and taking the rest
        entities["song"] = command.split("play")[1].strip()
    elif "play" in command and "youtube" in command:
        intent = "play_song"
        entities["platform"] = "youtube"
        entities["song"] = command.split("play")[1].replace("on youtube", "").strip()
    elif "search" in command:
        intent = "search"
        entities["query"] = command.split("search", 1)[1].strip()
    elif "shut down" in command:
        intent = "shutdown"
    elif "restart" in command:
        intent = "restart"

    return intent, entities

def execute_command(intent, entities):
    """Execute the parsed command."""
    if intent == "open":
        app = entities.get("application")
        if app == "spotify":
            speak("Opening Spotify.")
            spotify_path = r"C:\Users\SATYABRAT SAHU\AppData\Roaming\Spotify\Spotify.exe"  # Correct Spotify executable path
            subprocess.Popen(spotify_path)  # Open Spotify using the correct executable path
        elif app == "opera_gx":
            speak("Opening Opera GX.")
            opera_gx_path = r"C:\Users\SATYABRAT SAHU\OneDrive\Desktop\Opera GX Browser.lnk"  # Correct Opera GX executable path
            os.startfile(opera_gx_path)  # Opens the Opera GX browser shortcut
        elif app == "youtube":
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")  # Open YouTube in default browser (Opera GX)
        elif app == "gmail":
            speak("Opening Gmail.")
            webbrowser.open("https://mail.google.com")  # Open Gmail in default browser (Opera GX)
        elif app == "telegram":
            speak("Opening Telegram")
            webbrowser.open("https://www.telegram.com") # Open Telegram in default braowser (Opera GX)
        elif app == "vs code":
            speak("Opening vs code")
            vs_code_path = r"C:\Users\SATYABRAT SAHU\Downloads\VSCodeUserSetup-x64-1.80.2.exe" # Correct vs code executable path
            os.startfile(vs_code_path) # Opens the vs code shortcut 
        elif app == "discord":
            speak("Opening Discord")
            discord_path = r"C:\Users\SATYABRAT SAHU\OneDrive\Desktop\Discord.lnk" # Correct Discord path executable path 
            os.startfile(discord_path) # Opens the Discord shortcut 
    elif intent == "play_song":
        song = entities.get("song")
        if song:
            song == "youtube" and song
            speak(f"Playing {song} on YouTube.")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}")
    elif intent == "search":
        query = entities.get("query")
        if query:
            speak(f"Searching for {query} on GOOGLE for you.")
            webbrowser.open(f"https://www.google.com/search?q={query}")  # Open search in default browser (Opera GX)
    elif intent == "shutdown":
        speak("Shutting down the laptop. Goodbye!")
        os.system("shutdown /s /t 5")  # For Windows; adjust for other OS
    elif intent == "restart":
        speak("Restarting the laptop.")
        os.system("shutdown /r /t 5")  # For Windows; adjust for other OS
    else:
        speak("I don't understand that command.")

def main():
    """Main loop for the assistant."""
    speak("Hello! I am Jarvis, how can I help you?")
    while True:
        command = take_command()
        if command:
            if "exit" in command or "stop" in command:
                speak("Goodbye!")
                break
            intent, entities = parse_command(command)
            execute_command(intent, entities)

if __name__ == "__main__":
    main()
