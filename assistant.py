import os
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

def get_audio(activeListen):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if activeListen:
            playsound("chime.wav")
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception: " + str(e))
    print("I heard you say: " + said)
    return said

sp = SPT()

while True:
    text = get_audio(False)
    if "wake up" in text:
        activeListen = True
        speak("Hi Shanth, What can I help you with?")
        while activeListen:
            text = get_audio(True).strip()
            if any(x in text for x in ["what's the time", "what is the time"]):
                speak("The time is " + datetime.now().strftime("%I:%M %p"))
            elif any(x in text for x in ["today's date", "what's the date"]):
                speak("Today's date is " + datetime.now().strftime("%A, %B %d %Y"))
            elif text.endswith("on Spotify"):
                text = text.replace("on Spotify", "")
                while True:
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
                        newVolume = 100 if any(x in text.lower() for x in ["max", "100", "hundred"]) else 0 if any(x in text.lower() for x in ["min", "zero", " 0 "]) else 50 if any(x in text.lower() for x in ["half", "fifty", "50"]) else 0
                        sp.changeVolume(newVolume)
                    if any(x in text.lower() for x in ["exit spotify", "stop spotify"]):
                        break
                    text = get_audio(False).replace("on Spotify", "").strip()
            elif any(x in text for x in ["no", "go to sleep", "goodbye"]) and any(x not in text for x in ["yes", "yeah"]):
                speak("Goodbye Shanth")
                activeListen = False
                break
            else:
                speak("I'm sorry but I don't understand what you said")
                continue
            speak("Do you need anything else?")
