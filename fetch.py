# default imports
import os
import json
import requests
from pprint import pprint
from timeit import default_timer as timer

# custom imports
from scripts.extract import (
    get_track_data,
    get_track_features)

from scripts.utils import (
    output, 
    working_on,
    finished)

# external imports
output("Loading External Modules.")
import spotipy
import numpy as np
import pandas as pd
from tqdm import tqdm
from pprint import pprint

def main():
  # get data
  s = timer()
  his = pd.read_json( "data/StreamingHistory.json")

  # group by to find unique tracks 
  uniq_tracks = his.groupby(by=["artistName","trackName"])\
      .size().reset_index()[["artistName", "trackName"]]

  # convert to list of dicts
  uniq_tracks = uniq_tracks.to_dict('records')

  # load credentials 
  with open("credentials.json", "r") as f:
    creds = json.loads(f.read())
  finished("Loading Raw Data and Credentials", timer() - s)

  # connect to spotify dev app
  s = timer()
  token = spotipy.util.prompt_for_user_token(
      username=creds["username"],
      scope=creds["scope"],
      client_id=creds["client_id"],
      client_secret=creds["client_secret"],
      redirect_uri=creds["redirect_uri"])

  # connect to spotipy api
  sp = spotipy.Spotify(auth=token)
  finished("Connect to Spotipy API", timer() - s)

  s = working_on("Fetching Additional Track Data")
  i = 0
  tracks = [] 
  for track in tqdm(uniq_tracks):
    track_name = track["trackName"]
    artist_name = track["artistName"]
    track_data = track
    additional_data = get_track_data(
        track_name, artist_name, sp)
    
    if additional_data:
      track_id = additional_data["id"]
      track_features = get_track_features(track_id, sp)
      track_data.update(additional_data)

      if track_features:
        track_data.update(track_features)
      tracks.append(track_data)

  finished("Fetching Additional Track Data", timer() - s)

  # convert list of dicts into df
  tracks = pd.DataFrame(tracks)
  data = pd.merge(his, tracks, 
      on=["artistName", "trackName"],
      how="inner").reset_index()
  data.to_csv("data/StreamingHistory.csv", sep=",")

if __name__ == "__main__":
  main()
