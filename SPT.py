import os
import sys
import json
import spotipy
import spotipy.util as util

class SPT:
    scopes = "user-modify-playback-state user-read-playback-state user-read-currently-playing"

    def silence(func):
        def callAndSilence(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(e)
        return callAndSilence

    @silence
    def __init__(self):
        self.client = json.loads(open("client.json").read())
        try:
            token = util.prompt_for_user_token(self.client["username"], self.scopes, client_id=self.client["client_id"], client_secret=self.client["client_secret"], redirect_uri=self.client["redirect_uri"])
        except:
            os.remove(f".cache-{self.client['username']}")
            token = util.prompt_for_user_token(self.client["username"], self.scopes, client_id=self.client["client_id"], client_secret=self.client["client_secret"], redirect_uri=self.client["redirect_uri"])
        self.sp = spotipy.Spotify(auth=token)
        self.setActiveDevice(self.client["primary_device_name"])

    @silence
    def setActiveDevice(self, device_name):
        response = self.sp.devices()
        for device in response["devices"]:
            if device["name"] == device_name:
                self.deviceID = device["id"]

    @silence
    def playTrackByName(self, trackName, artistName):
        query = f"track:{trackName}" + (f" artist: {artistName}" if artistName else "")
        print(query)
        response = self.sp.search(query, limit=1, offset=0, type="track")
        trackURI = response["tracks"]["items"][0]["uri"]
        self.sp.start_playback(uris=[trackURI], device_id=self.deviceID)

    @silence
    def resumeTrack(self):
        self.sp.start_playback(device_id=self.deviceID)

    @silence
    def pauseTrack(self):
        self.sp.pause_playback(device_id=self.deviceID)

    @silence
    def seekToPosition(self, position_ms):
        self.sp.seek_track(position_ms, device_id=self.deviceID)

    @silence
    def changeVolume(self, volume):
        self.sp.volume(volume, device_id=self.deviceID)
