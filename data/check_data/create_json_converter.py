"""
This file takes a file containing a csv structured as ``spotify_id,spotify_id``
and creates a json file containing the retrieved info from spotify and the audio
features
"""
import json
from typing import Optional, Dict
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CONVERSION_TEXT_PATH = "./conversion.txt"


def get_spotify_keys(path: str = "./spotify_keys.txt") -> Optional[Dict[str,
                                                                        str]]:
    """
    Function that reads a file where are stored a pair of spotify keys
    Parameters
    -------
    path: str
        path to the file containing the credential keys.
    Returns
    -------
    Dict[str: str]
        return a dictionary with keys "clientID" and "client_secret", whose
        values are the effective keys.
    """
    try:
        with open(path, "r") as spotify_keys:
            client_keys = dict()
            for key_string in spotify_keys.readlines():
                key, value = key_string.strip().split(": ")
                client_keys[key] = value
        return client_keys
    except FileNotFoundError as error:
        print(error,
              "You don't have a file named 'spotify_keys.txt'"
              " that should contain both API keys!")
        return None


keys = get_spotify_keys("./../../spotify_info/spotify_keys.txt")

# Create credential for the api
credentials = SpotifyClientCredentials(client_id=keys["clientID"],
                                       client_secret=keys["client_secret"])
# Instantiate the API
sp = spotipy.Spotify(client_credentials_manager=credentials)

wrong_ids = []
right_ids = []
with open(CONVERSION_TEXT_PATH, "r", encoding="utf8") as conv:
    conv = conv.readlines()
    for line in conv:
        old_id, new_id = line.split(",")
        wrong_ids.append(old_id.strip())
        right_ids.append(new_id.strip())

right_sp_info = sp.tracks(right_ids)
features_list = sp.audio_features(right_ids)

conversion_dict = {}
for w_id, sp_info, features in zip(wrong_ids, right_sp_info, features_list):
    conversion_dict[w_id] = {"info": sp_info, "feats": features_list}

with open("conversion.json", "w", encoding="utf8") as outfile:
    json.dump(conversion_dict, outfile)
