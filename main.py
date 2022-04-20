# default imports
import os
import json
import requests

# custom imports
from scripts import (
    get_track_data,
    get_track_features)

# external imports
import spotipy
import numpy as np
import pandas as pd
from tqdm import tqdm

def get_id(track_name, token):
  headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}',
    }

  params = [
    ('q', track_name),
    ('type', 'track'),
    ]
  
  res = requests.get(
      'https://api.spotify.com/v1/search', 
      headers = headers, 
      params = params, 
      timeout = 5)

  res = res.json()
  print(res)
  first_result = res['tracks']['items'][0]
  track_id = first_result['id']

  return track_id

def main():
  # get data
  data = pd.read_json("data/sample-streaming-history.json")

  # load credentials 
  with open("credentials.json", "r") as f:
    creds = json.loads(f.read())

  # connect to spotify dev app
  token = spotipy.util.prompt_for_user_token(
      username=creds["username"],
      scope=creds["scope"],
      client_id=creds["client_id"],
      client_secret=creds["client_secret"],
      redirect_uri=creds["redirect_uri"])

  i = 0
  for idx, track in tqdm(data.iterrows()):
    track_name = track['trackName']
    artist_name = track['artistName']
    track_data = get_track_data(
        track_name, artist_name, token)
    if track_data:
      track_id = track_data['id']
      track_features = get_track_features(track_id, token)
      print(idx)
      i+=1
  print(i)

if __name__ == "__main__":
  main()
