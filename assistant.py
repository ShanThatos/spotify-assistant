import os
import time
import speech_recognition as sr
from datetime import datetime
from playsound import playsound
from gtts import gTTS
from SPT import SPT

def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")
    playsound("temp.mp3")
    os.remove("temp.mp3")

current_state = "SLEEP"
sp = None
rgn = sr.Recognizer()
rgn.energy_threshold = 3000
rgn.dynamic_energy_threshold = True
rgn.pause_threshold = .5
mic = sr.Microphone()
stop_listening = None

with mic as source:
    rgn.adjust_for_ambient_noise(source)

def callback(rgn, audio):
    global current_state
    global sp
    global stop_listening
    text = ""
    try:
        text = rgn.recognize_google(audio)
    except sr.UnknownValueError:
        if current_state == "ACTIVE":
            speak("I'm sorry but I did not understand what you said")
        return
    except Exception as e:
        print(e)
        return
    print(f"I heard you say: '{text}'")
    if current_state == "SLEEP" and "wake up" in text:
        text = text.replace("wake up", "").strip()
        current_state = "ACTIVE"
        speak("Hi Shanth, what can I help you with?")
        playsound("chime.wav")
    elif current_state == "ACTIVE":
        if any(x in text for x in ["what's the time", "what is the time"]):
            speak("The time is " + datetime.now().strftime("%I:%M %p"))
            speak("Do you need anything else?")
            playsound("chime.wav")
        elif any(x in text for x in ["today's date", "what's the date"]):
            speak("Today's date is " + datetime.now().strftime("%A, %B %d %Y"))
            speak("Do you need anything else?")
            playsound("chime.wav")
        elif any(x in text.lower() for x in ["start spotify", "open spotify", "connect to spotify", "on spotify", "spotify"]):
            if not sp:
                sp = SPT()
            current_state = "SPOTIFY"
            speak("What would you like to do in Spotify?")
            playsound("chime.wav")
        elif any(x in text for x in ["no", "go to sleep", "goodbye"]) and any(x not in text for x in ["yes", "yeah"]):
            speak("Goodbye Shanth")
    elif current_state == "SPOTIFY":
        if "play" in text.lower():
            if not text.lower().replace("play", "").strip():
                sp.resumeTrack()
            for song_command in ["can you play the song", "can you play", "play the song", "play", "Play"]:
                if song_command in text:
                    text = text.replace(song_command, "")
                    if " by " in text:
                        text = text.split(" by ")
                        sp.playTrackByName(text[0], text[1])
                        text = ""
                    else:
                        sp.playTrackByName(text, None)
                    break
        if "resume" in text.lower():
            sp.resumeTrack()
        if "pause" in text.lower():
            sp.pauseTrack()
        if "restart" in text.lower():
            sp.seekToPosition(0)
            sp.resumeTrack()
        if "volume" in text.lower():
            newVolume = 100 if any(x in text.lower() for x in ["full", "max", "100", "hundred"]) else 0 if any(x in text.lower() for x in ["min", "zero", " 0 "]) else 50 if any(x in text.lower() for x in ["half", "fifty", "50"]) else 0
            sp.changeVolume(newVolume)
        if any(x in text.lower() for x in ["exit spotify", "stop spotify"]):
            current_state = "ACTIVE"

stop_listening = rgn.listen_in_background(mic, callback)

while current_state:
    time.sleep(.1)
