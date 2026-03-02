
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import time

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

_token = None
_token_expires = 0

def get_token():
    global _token, _token_expires
    if time.time() > _token_expires:
        auth_string = client_id + ":" + client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        if result.status_code != 200:
            # Or raise an exception
            return None
        json_result = result.json()
        _token = json_result.get("access_token")
        # Subtract 60 seconds for a buffer
        _token_expires = time.time() + json_result.get("expires_in", 3600) - 60
    return _token

def get_auth_header():
    token = get_token()
    if not token:
        return None
    return {"Authorization": "Bearer " + token}

def search_for_artist(artist_name):
    headers = get_auth_header()
    if headers is None:
        return None
    url = "https://api.spotify.com/v1/search"
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content).get("artists", {}).get("items")
    if not json_result:
        print("Nothing found...")
        return None
    
    return json_result[0]

def get_songs_by_artist(artist_id):
    headers = get_auth_header()
    if headers is None:
        return None
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    result = get(url, headers=headers)
    json_result = json.loads(result.content).get("tracks")
    return json_result

def search_for_song(song_name):
    headers = get_auth_header()
    if headers is None:
        return None
    url = "https://api.spotify.com/v1/search"
    query = f"?q={song_name}&type=track&limit=10"

    query_url = url + query
    
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content).get("tracks", {}).get("items")
    if not json_result:
        print("Nothing found...")
        return None
    return json_result
